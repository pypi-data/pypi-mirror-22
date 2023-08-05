# -*- coding: utf-8 -*-

from __future__ import division

import csv
import json
import logging
import pkg_resources

from numpy import ceil, fromiter, int16, logical_or as or_, logical_and as and_, take

import openfisca_france
from openfisca_core.periods import Instant

from openfisca_france.model.base import *  # noqa  analysis:ignore
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf
from openfisca_france.model.caracteristiques_socio_demographiques.logement import statut_occupation_logement

log = logging.getLogger(__name__)

zone_apl_by_depcom = None


class al_nb_personnes_a_charge(Variable):
    column = IntCol
    entity = Famille
    label = u"Nombre de personne à charge au sens des allocations logement"
    definition_period = MONTH

    def function(famille, period, legislation):
        '''
        site de la CAF en 2011:

        # Enfant à charge
        Vous assurez financièrement l'entretien et asez la responsabilité
        affective et éducative d'un enfant, que vous ayez ou non un lien de
        parenté avec lui. Il est reconnu à votre charge pour le versement
        des aides au logement jusqu'au mois précédent ses 21 ans.
        Attention, s'il travaille, il doit gagner moins de 836,55 € par mois.

        # Parents âgés ou infirmes
        Sont à votre charge s'ils vivent avec vous et si leurs revenus 2009
        ne dépassent pas 10 386,59 € :
        * vos parents ou grand-parents âgés de plus de 65 ans ou d'au moins
        60 ans, inaptes au travail, anciens déportés,
        * vos proches parents infirmes âgés de 22 ans ou plus (parents,
        grand-parents, enfants, petits enfants, frères, soeurs, oncles,
        tantes, neveux, nièces).
        '''

        age_max_enfant = legislation(period).prestations.prestations_familiales.cf.age_max
        residence_dom = famille.demandeur.menage('residence_dom', period)

        def al_nb_enfants():
            age_min_enfant = legislation(period).prestations.prestations_familiales.af.age1
            return nb_enf(famille, period, age_min_enfant, age_max_enfant - 1)  # La limite sur l'age max est stricte.

        def al_nb_adultes_handicapes():

            # Variables à valeur pour un individu
            base_ressources_i = famille.members('prestations_familiales_base_ressources_individu', period)
            inapte_travail = famille.members('inapte_travail', period)
            taux_incapacite = famille.members('taux_incapacite', period)
            age = famille.members('age', period)

            # Parametres
            plafond_ressource = legislation(period.n_2.stop).prestations.minima_sociaux.aspa.plafond_ressources_seul * 1.25
            taux_incapacite_minimum = 0.8

            adulte_handicape = (
                ((taux_incapacite > taux_incapacite_minimum) + inapte_travail) *
                (age >= age_max_enfant) *
                (base_ressources_i <= plafond_ressource)
                )

            # Par convention les adultes handicapé à charge de la famille ont le role ENFANT dans la famille
            # Le demandeur et son conjoint ne sont jamais considérés comme à charge
            return famille.sum(adulte_handicape, role = Famille.ENFANT)

        nb_pac = al_nb_enfants() + al_nb_adultes_handicapes()
        nb_pac = where(residence_dom, min_(nb_pac, 6), nb_pac)
        # Dans les DOMs, le barème est fixe à partir de 6 enfants.

        return nb_pac


class al_couple(Variable):
    column = BoolCol
    entity = Famille
    label = u'Situation de couple pour le calcul des AL'
    definition_period = MONTH

    def function(self, simulation, period):
        en_couple = simulation.calculate('en_couple', period)
        enceinte = simulation.calculate('enceinte_fam', period)
        couple = en_couple + enceinte  # le barème "couple" est utilisé pour les femmes enceintes isolées

        return couple


class aide_logement_base_ressources_eval_forfaitaire(Variable):
    column = FloatCol
    entity = Famille
    label = u"Base ressources en évaluation forfaitaire des aides au logement (R351-7 du CCH)"
    definition_period = MONTH

    def function(self, simulation, period):
        def eval_forfaitaire_salaries():
            salaire_imposable_holder = simulation.compute('salaire_imposable', period.offset(-1))
            salaire_imposable = self.sum_by_entity(salaire_imposable_holder, roles = [CHEF, PART])
            # Application de l'abattement pour frais professionnels
            params_abattement = simulation.legislation_at(period.start).impot_revenu.tspr.abatpro
            somme_salaires_mois_precedent = 12 * salaire_imposable
            montant_abattement = round_(
                min_(
                    max_(params_abattement.taux * somme_salaires_mois_precedent, params_abattement.min),
                    params_abattement.max
                    )
                )
            return max_(0, somme_salaires_mois_precedent - montant_abattement)

        def eval_forfaitaire_tns():
            last_july_first = Instant(
                (period.start.year if period.start.month >= 7 else period.start.year - 1,
                7, 1))
            smic_horaire_brut = simulation.legislation_at(last_july_first).cotsoc.gen.smic_h_b
            travailleur_non_salarie_holder = simulation.compute('travailleur_non_salarie', period)
            any_tns = self.any_by_roles(travailleur_non_salarie_holder)
            return any_tns * 1500 * smic_horaire_brut

        return max_(eval_forfaitaire_salaries(), eval_forfaitaire_tns())


class aide_logement_abattement_chomage_indemnise(Variable):
    column = FloatCol
    entity = Individu
    label = u"Montant de l'abattement pour personnes au chômage indemnisé (R351-13 du CCH)"
    definition_period = MONTH

    def function(self, simulation, period):
        chomage_net_m_1 = simulation.calculate('chomage_net', period.offset(-1))
        chomage_net_m_2 = simulation.calculate('chomage_net', period.offset(-2))
        revenus_activite_pro = simulation.calculate_add('salaire_imposable', period.n_2)
        taux_abattement = simulation.legislation_at(period.start).prestations.aides_logement.ressources.abattement_chomage_indemnise
        taux_frais_pro = simulation.legislation_at(period.start).impot_revenu.tspr.abatpro.taux

        abattement = and_(chomage_net_m_1 > 0, chomage_net_m_2 > 0) * taux_abattement * revenus_activite_pro
        abattement = round_((1 - taux_frais_pro) * abattement)

        return abattement


class aide_logement_abattement_depart_retraite(Variable):
    column = FloatCol
    entity = Individu
    label = u"Montant de l'abattement sur les salaires en cas de départ en retraite"
    definition_period = MONTH

    def function(self, simulation, period):
        retraite = simulation.calculate('activite', period) == 3
        activite_n_2 = simulation.calculate_add('salaire_imposable', period.n_2)
        retraite_n_2 = simulation.calculate('retraite_imposable', period.n_2)
        taux_frais_pro = simulation.legislation_at(period.start).impot_revenu.tspr.abatpro.taux

        abattement = 0.3 * activite_n_2 * (retraite_n_2 == 0) * retraite
        abattement = round_((1 - taux_frais_pro) * abattement)

        return abattement


class aide_logement_neutralisation_rsa(Variable):
    column = FloatCol
    entity = Famille
    label = u"Abattement sur les revenus n-2 pour les bénéficiaires du RSA"
    definition_period = MONTH

    def function(self, simulation, period):
        # Circular definition, as rsa depends on al.
        # We don't allow it, so default value of rsa will be returned if a recursion is detected.
        rsa_last_month = simulation.calculate('rsa', period.last_month, max_nb_cycles = 0)
        activite = simulation.compute_add('salaire_imposable', period.n_2)
        chomage = simulation.compute_add('chomage_imposable', period.n_2)
        activite_n_2 = self.sum_by_entity(activite)
        chomage_n_2 = self.sum_by_entity(chomage)
        taux_frais_pro = simulation.legislation_at(period.start).impot_revenu.tspr.abatpro.taux

        abattement = (activite_n_2 + chomage_n_2) * rsa_last_month
        abattement = round_((1 - taux_frais_pro) * abattement)

        return abattement


class aide_logement_base_ressources_defaut(Variable):
    column = FloatCol
    entity = Famille
    label = u"Base ressource par défaut des allocations logement"
    definition_period = MONTH

    def function(self, simulation, period):
        biactivite = simulation.calculate('biactivite', period)
        Pr = simulation.legislation_at(period.start).prestations.aides_logement.ressources
        base_ressources_holder = simulation.compute('prestations_familiales_base_ressources_individu', period)
        base_ressources_parents = self.sum_by_entity(base_ressources_holder, roles = [CHEF, PART])
        abattement_chomage_indemnise_holder = simulation.compute('aide_logement_abattement_chomage_indemnise', period)
        abattement_chomage_indemnise = self.sum_by_entity(abattement_chomage_indemnise_holder, roles = [CHEF, PART])
        abattement_depart_retraite_holder = simulation.compute('aide_logement_abattement_depart_retraite', period)
        abattement_depart_retraite = self.sum_by_entity(abattement_depart_retraite_holder, roles = [CHEF, PART])
        neutralisation_rsa = simulation.calculate('aide_logement_neutralisation_rsa', period)
        abattement_ressources_enfant = simulation.legislation_at(period.n_2.stop).prestations.minima_sociaux.aspa.plafond_ressources_seul * 1.25
        base_ressources_enfants = self.sum_by_entity(
            max_(0, base_ressources_holder.array - abattement_ressources_enfant), roles = ENFS)

        # Revenus du foyer fiscal
        rev_coll = simulation.famille.demandeur.foyer_fiscal('rev_coll', period.n_2)

        ressources = (
            base_ressources_parents + base_ressources_enfants + rev_coll -
            (abattement_chomage_indemnise + abattement_depart_retraite + neutralisation_rsa)
            )

        # Abattement forfaitaire pour double activité
        abattement_double_activite = biactivite * Pr.dar_1

        # Arrondi aux 100 euros supérieurs
        result = max_(ressources - abattement_double_activite, 0)

        return result


class aide_logement_base_ressources(Variable):
    column = FloatCol
    entity = Famille
    label = u"Base ressources des allocations logement"
    definition_period = MONTH

    def function(self, simulation, period):
        mois_precedent = period.offset(-1)
        last_day_reference_year = period.n_2.stop
        base_ressources_defaut = simulation.calculate('aide_logement_base_ressources_defaut', period)
        base_ressources_eval_forfaitaire = simulation.calculate(
            'aide_logement_base_ressources_eval_forfaitaire', period)
        en_couple = simulation.calculate('en_couple', period)
        aah_holder = simulation.compute('aah', mois_precedent)
        aah = self.sum_by_entity(aah_holder, roles = [CHEF, PART])
        age_holder = simulation.compute('age', period)
        age = self.split_by_roles(age_holder, roles = [CHEF, PART])
        smic_horaire_brut_n2 = simulation.legislation_at(last_day_reference_year).cotsoc.gen.smic_h_b
        salaire_imposable_holder = simulation.compute('salaire_imposable', period.offset(-1))
        somme_salaires = self.sum_by_entity(salaire_imposable_holder, roles = [CHEF, PART])

        plafond_eval_forfaitaire = 1015 * smic_horaire_brut_n2

        plafond_salaire_jeune_isole = simulation.legislation_at(period.start).prestations.aides_logement.ressources.dar_8
        plafond_salaire_jeune_couple = simulation.legislation_at(period.start).prestations.aides_logement.ressources.dar_9
        plafond_salaire_jeune = where(en_couple, plafond_salaire_jeune_couple, plafond_salaire_jeune_isole)

        neutral_jeune = or_(age[CHEF] < 25, and_(en_couple, age[PART] < 25))
        neutral_jeune &= somme_salaires < plafond_salaire_jeune

        eval_forfaitaire = base_ressources_defaut <= plafond_eval_forfaitaire
        eval_forfaitaire &= base_ressources_eval_forfaitaire > 0
        eval_forfaitaire &= aah == 0
        eval_forfaitaire &= not_(neutral_jeune)

        ressources = where(eval_forfaitaire, base_ressources_eval_forfaitaire, base_ressources_defaut)

        # Planchers de ressources pour étudiants
        # Seul le statut étudiant (et boursier) du demandeur importe, pas celui du conjoint
        Pr = simulation.legislation_at(period.start).prestations.aides_logement.ressources
        etudiant_holder = simulation.compute('etudiant', period)
        boursier_holder = simulation.compute('boursier', period)
        etudiant = self.split_by_roles(etudiant_holder, roles = [CHEF, PART])
        boursier = self.split_by_roles(boursier_holder, roles = [CHEF, PART])
        montant_plancher_ressources = max_(0, etudiant[CHEF] * Pr.dar_4 - boursier[CHEF] * Pr.dar_5)
        ressources = max_(ressources, montant_plancher_ressources)

        # Arrondi au centime, pour éviter qu'une petite imprécision liée à la recombinaison d'une valeur annuelle éclatée ne fasse monter d'un cran l'arrondi au 100€ supérieur.

        ressources = round_(ressources * 100) / 100

        # Arrondi aux 100 euros supérieurs
        ressources = ceil(ressources / 100) * 100

        return ressources


class aide_logement_loyer_plafond(Variable):
    column = FloatCol
    entity = Famille
    label = u"Loyer plafond dans le calcul des aides au logement (L2)"
    definition_period = MONTH

    def function(famille, period, legislation):
        al = legislation(period).prestations.aides_logement
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)
        coloc = famille.demandeur.menage('coloc', period)
        chambre = famille.demandeur.menage('logement_chambre', period)
        zone_apl = famille.demandeur.menage('zone_apl', period)

        # Preprocessing pour pouvoir accéder aux paramètres dynamiquement par zone.
        plafonds_by_zone = [
            [0] +
            [al.loyers_plafond['zone' + str(zone)][i]
            for zone in range(1, 4)]
            for i in ['personnes_seules', 'couples', 'un_enfant', 'majoration_par_enf_supp']
            ]
        plafond_personne_seule = take(plafonds_by_zone[0], zone_apl)
        plafond_couple = take(plafonds_by_zone[1], zone_apl)
        plafond_famille = take(plafonds_by_zone[2], zone_apl) + (al_nb_pac > 1) * (al_nb_pac - 1) * take(plafonds_by_zone[3], zone_apl)

        plafond = select(
            [not_(couple) * (al_nb_pac == 0) + chambre, al_nb_pac > 0],
            [plafond_personne_seule, plafond_famille],
            default = plafond_couple
            )

        coeff_coloc = where(coloc, al.loyers_plafond.colocation, 1)
        coeff_chambre = where(chambre, al.loyers_plafond.chambre, 1)

        return round_(plafond * coeff_coloc * coeff_chambre, 2)


class aide_logement_loyer_seuil_degressivite(Variable):
    column = FloatCol
    entity = Famille
    label = u"Seuil de degressivité dans le calcul des aides au logement"
    start_date = date(2016, 7, 1)
    definition_period = MONTH

    def function(famille, period, legislation):
        al = legislation(period).prestations.aides_logement
        zone_apl = famille.demandeur.menage('zone_apl', period)
        loyer_plafond = famille('aide_logement_loyer_plafond', period)
        chambre = famille.demandeur.menage('logement_chambre', period)
        coloc = famille.demandeur.menage('coloc', period)

        coeff_degressivite_by_zone = [0] + [al.loyers_plafond['zone' + str(zone)]['degressivite'] for zone in range(1, 4)]
        coeff_degressivite = take(coeff_degressivite_by_zone, zone_apl)

        loyer_degressivite = loyer_plafond * coeff_degressivite
        minoration_coloc = loyer_degressivite * 0.25 * coloc
        minoration_chambre = loyer_degressivite * 0.1 * chambre
        loyer_degressivite -= minoration_coloc + minoration_chambre

        return round_(loyer_degressivite, 2)


class aide_logement_loyer_seuil_suppression(Variable):
    column = FloatCol
    entity = Famille
    label = u"Seuil de suppression dans le calcul des aides au logement"
    start_date = date(2016, 7, 1)
    definition_period = MONTH

    def function(famille, period, legislation):
        al = legislation(period).prestations.aides_logement
        zone_apl = famille.demandeur.menage('zone_apl', period)
        loyer_plafond = famille('aide_logement_loyer_plafond', period)
        chambre = famille.demandeur.menage('logement_chambre', period)
        coloc = famille.demandeur.menage('coloc', period)

        coeff_suppression_by_zone = [0] + [al.loyers_plafond['zone' + str(zone)]['suppression'] for zone in range(1, 4)]
        coeff_suppression = take(coeff_suppression_by_zone, zone_apl)

        loyer_suppression = loyer_plafond * coeff_suppression
        minoration_coloc = loyer_suppression * 0.25 * coloc
        minoration_chambre = loyer_suppression * 0.1 * chambre
        loyer_suppression -= minoration_coloc + minoration_chambre

        return round_(loyer_suppression, 2)


class aide_logement_loyer_reel(Variable):
    column = FloatCol
    entity = Famille
    label = u"Loyer réel dans le calcul des aides au logement"
    definition_period = MONTH

    def function(famille, period):
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        loyer = famille.demandeur.menage('loyer', period)
        coeff_meuble = where(statut_occupation_logement == 5, 2 / 3, 1)  # Coeff de 2/3 pour les meublés
        return round_(loyer * coeff_meuble)


class aide_logement_loyer_retenu(Variable):
    column = FloatCol
    entity = Famille
    label = u"Loyer retenu (hors charge) dans le calcul des aides au logement"
    definition_period = MONTH

    def function(famille, period, legislation):
        al = legislation(period).prestations.aides_logement
        loyer_plafond = famille('aide_logement_loyer_plafond', period)
        loyer_reel = famille('aide_logement_loyer_reel', period)

        # loyer retenu
        return min_(loyer_reel, loyer_plafond)


class aide_logement_charges(Variable):
    column = FloatCol
    entity = Famille
    label = u"Charges retenues dans le calcul des aides au logement"
    definition_period = MONTH

    def function(famille, period, legislation):
        P = legislation(period).prestations.aides_logement.forfait_charges
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)
        coloc = famille.demandeur.menage('coloc', period)
        montant_coloc = where(couple, 1, 0.5) * P.cas_general + al_nb_pac * P.majoration_par_enfant
        montant_cas_general = P.cas_general + al_nb_pac * P.majoration_par_enfant

        return where(coloc, montant_coloc, montant_cas_general)


class aide_logement_R0(DatedVariable):
    column = FloatCol
    entity = Famille
    label = u"Revenu de référence, basé sur la situation familiale, pris en compte dans le calcul des AL."
    definition_period = MONTH

    @dated_function(stop = date(2014, 12, 31))
    def function_2014(famille, period, legislation):
        al = legislation(period).prestations.aides_logement
        pfam_n_2 = legislation(period.start.offset(-2, 'year')).prestations.prestations_familiales
        minim_n_2 = legislation(period.start.offset(-2, 'year')).prestations.minima_sociaux
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        residence_dom = famille.demandeur.menage('residence_dom', period)

        n_2 = period.start.offset(-2, 'year')
        if n_2.date >= date(2009, 6, 01):
            montant_de_base = minim_n_2.rsa.montant_de_base_du_rsa
        else:
            montant_de_base = minim_n_2.rmi.montant_de_base_du_rmi

        R1 = montant_de_base * (
            al.r1.personne_isolee * not_(couple) * (al_nb_pac == 0) +
            al.r1.couple_sans_enf * couple * (al_nb_pac == 0) +
            al.r1.personne_isolee_ou_couple_avec_1_enf * (al_nb_pac == 1) +
            al.r1.personne_isolee_ou_couple_avec_2_enf * (al_nb_pac >= 2) +
            al.r1.majoration_enfant_a_charge_supp * (al_nb_pac > 2) * (al_nb_pac - 2)
            )

        R2 = pfam_n_2.af.bmaf * (
            al.r2.taux3_dom * residence_dom * (al_nb_pac == 1) +
            al.r2.personnes_isolees_ou_couples_avec_2_enf * (al_nb_pac >= 2) +
            al.r2.majoration_par_enf_supp_a_charge * (al_nb_pac > 2) * (al_nb_pac - 2)
            )

        R0 = round_(12 * (R1 - R2) * (1 - al.autres.abat_sal))

        return R0

    # cf Décret n° 2014-1739 du 29 décembre 2014 relatif au calcul des aides personnelles au logement
    @dated_function(start = date(2015, 1, 1))
    def function_2015(famille, period, legislation):
        al = legislation(period).prestations.aides_logement
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)

        R0 = (
            al.R0.taux_seul * not_(couple) * (al_nb_pac == 0) +
            al.R0.taux_couple * couple * (al_nb_pac == 0) +
            al.R0.taux1pac * (al_nb_pac == 1) +
            al.R0.taux2pac * (al_nb_pac == 2) +
            al.R0.taux3pac * (al_nb_pac == 3) +
            al.R0.taux4pac * (al_nb_pac == 4) +
            al.R0.taux5pac * (al_nb_pac == 5) +
            al.R0.taux6pac * (al_nb_pac == 6) +
            al.R0.taux_pac_supp * (al_nb_pac > 6) * (al_nb_pac - 6)
            )

        return R0


class aide_logement_taux_famille(Variable):
    column = FloatCol
    entity = Famille
    label = u"Taux représentant la situation familiale, décroissant avec le nombre de personnes à charge"
    definition_period = MONTH

    def function(famille, period, legislation):
        al = legislation(period).prestations.aides_logement
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        residence_dom = famille.demandeur.menage('residence_dom', period)

        TF_metropole = (
            al.taux_participation_fam.taux_1_adulte * (not_(couple)) * (al_nb_pac == 0) +
            al.taux_participation_fam.taux_2_adulte * (couple) * (al_nb_pac == 0) +
            al.taux_participation_fam.taux_1_enf * (al_nb_pac == 1) +
            al.taux_participation_fam.taux_2_enf * (al_nb_pac == 2) +
            al.taux_participation_fam.taux_3_enf * (al_nb_pac == 3) +
            al.taux_participation_fam.taux_4_enf * (al_nb_pac >= 4) +
            al.taux_participation_fam.taux_enf_supp * (al_nb_pac > 4) * (al_nb_pac - 4)
            )

        TF_dom = (
            al.taux_participation_fam.dom.taux1 * (not_(couple)) * (al_nb_pac == 0) +
            al.taux_participation_fam.dom.taux2 * (couple) * (al_nb_pac == 0) +
            al.taux_participation_fam.dom.taux3 * (al_nb_pac == 1) +
            al.taux_participation_fam.dom.taux4 * (al_nb_pac == 2) +
            al.taux_participation_fam.dom.taux5 * (al_nb_pac == 3) +
            al.taux_participation_fam.dom.taux6 * (al_nb_pac == 4) +
            al.taux_participation_fam.dom.taux7 * (al_nb_pac == 5) +
            al.taux_participation_fam.dom.taux8 * (al_nb_pac >= 6)
            )

        return where(residence_dom, TF_dom, TF_metropole)


class aide_logement_taux_loyer(Variable):
    column = FloatCol
    entity = Famille
    label = u"Taux obscur basé sur une comparaison du loyer retenu à un loyer de référence."
    definition_period = MONTH

    def function(self, simulation, period):
        al = simulation.legislation_at(period.start).prestations.aides_logement
        z2 = al.loyers_plafond.zone2

        L = simulation.calculate('aide_logement_loyer_retenu', period)
        couple = simulation.calculate('al_couple', period)
        al_nb_pac = simulation.calculate('al_nb_personnes_a_charge', period)

        loyer_reference = (
            z2.personnes_seules * (not_(couple)) * (al_nb_pac == 0) +
            z2.couples * (couple) * (al_nb_pac == 0) +
            z2.un_enfant * (al_nb_pac >= 1) +
            z2.majoration_par_enf_supp * (al_nb_pac > 1) * (al_nb_pac - 1)
            )

        RL = L / loyer_reference

        # TODO: paramètres en dur ??
        TL = where(RL >= 0.75,
            al.taux_participation_loyer.taux_tranche_3 * (RL - 0.75) + al.taux_participation_loyer.taux_tranche_2 * (0.75 - 0.45),
            max_(0, al.taux_participation_loyer.taux_tranche_2 * (RL - 0.45))
            )

        return TL


class aide_logement_participation_personnelle(Variable):
    column = FloatCol
    entity = Famille
    label = u"Participation personelle de la famille au loyer"
    definition_period = MONTH

    def function(self, simulation, period):

        al = simulation.legislation_at(period.start).prestations.aides_logement

        R = simulation.calculate('aide_logement_base_ressources', period)
        R0 = simulation.calculate('aide_logement_R0', period)
        Rp = max_(0, R - R0)

        loyer_retenu = simulation.calculate('aide_logement_loyer_retenu', period)
        charges_retenues = simulation.calculate('aide_logement_charges', period)
        E = loyer_retenu + charges_retenues
        P0 = max_(al.participation_min.taux * E, al.participation_min.montant_forfaitaire)  # Participation personnelle minimale

        Tf = simulation.calculate('aide_logement_taux_famille', period)
        Tl = simulation.calculate('aide_logement_taux_loyer', period)
        Tp = Tf + Tl  # Taux de participation

        return P0 + Tp * Rp


class aide_logement_montant_brut_avant_degressivite(Variable):
    column = FloatCol
    label = u"Montant des aides aux logements en secteur locatif avant degressivité et brut de CRDS"
    entity = Famille
    definition_period = MONTH

    def function(famille, period, legislation):
        al = legislation(period).prestations.aides_logement
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        locataire = ((3 <= statut_occupation_logement) * (5 >= statut_occupation_logement)) + (statut_occupation_logement == 7)
        accedant = (statut_occupation_logement == 1)

        loyer_retenu = famille('aide_logement_loyer_retenu', period)
        charges_retenues = famille('aide_logement_charges', period)
        participation_personnelle = famille('aide_logement_participation_personnelle', period)

        montant_locataire = max_(0, loyer_retenu + charges_retenues - participation_personnelle)
        montant_accedants = 0  # TODO: APL pour les accédants à la propriété

        montant = select([locataire, accedant], [montant_locataire, montant_accedants])

        montant = montant * (montant >= al.al_min.montant_min_mensuel.montant_min_apl_al)  # Montant minimal de versement

        return montant


class aide_logement_montant_brut(DatedVariable):
    column = FloatCol
    entity = Famille
    label = u"Montant des aides au logement après degressivité, avant CRDS"
    definition_period = MONTH

    @dated_function(stop = date(2016, 6, 30))
    def function_avant_degression(famille, period):
        montant_avant_degressivite = famille('aide_logement_montant_brut_avant_degressivite', period)
        return montant_avant_degressivite

    @dated_function(start = date(2016, 7, 1))
    def function_apres_degression(famille, period):
        montant_avant_degressivite = famille('aide_logement_montant_brut_avant_degressivite', period)
        loyer_reel = famille('aide_logement_loyer_reel', period)
        loyer_degressivite = famille('aide_logement_loyer_seuil_degressivite', period)
        loyer_suppression = famille('aide_logement_loyer_seuil_suppression', period)
        handicap_i = famille.members('handicap', period)
        handicap = famille.any(handicap_i)

        coeff = select(
            [loyer_reel <= loyer_degressivite, loyer_reel <= loyer_suppression, loyer_reel > loyer_suppression],
            [1, 1 - ((loyer_reel - loyer_degressivite) / (loyer_suppression - loyer_degressivite)), 0]
            )

        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        accedant = (statut_occupation_logement == 1)
        locataire_foyer = (statut_occupation_logement == 7)
        exception = accedant + locataire_foyer + handicap
        coeff = where(exception, 1, coeff)

        montant = round_(montant_avant_degressivite * coeff, 2)

        return montant


class aide_logement_montant(Variable):
    column = FloatCol
    entity = Famille
    label = u"Montant des aides au logement net de CRDS"
    definition_period = MONTH

    def function(self, simulation, period):
        aide_logement_montant_brut = simulation.calculate('aide_logement_montant_brut', period)
        crds_logement = simulation.calculate('crds_logement', period)
        montant = round_(aide_logement_montant_brut + crds_logement, 2)

        return montant


class alf(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Famille
    label = u"Allocation logement familiale"
    url = u"http://vosdroits.service-public.fr/particuliers/F13132.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def function(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        proprietaire_proche_famille = famille('proprietaire_proche_famille', period)

        result = (al_nb_pac >= 1) * (statut_occupation_logement != 3) * not_(proprietaire_proche_famille) * aide_logement_montant
        return result


class als_non_etudiant(Variable):
    column = FloatCol
    entity = Famille
    label = u"Allocation logement sociale (non étudiante)"
    definition_period = MONTH

    def function(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        proprietaire_proche_famille = famille('proprietaire_proche_famille', period)

        etudiant = famille.members('etudiant', period)
        no_parent_etudiant = not_(famille.any(etudiant, role = Famille.PARENT))

        return (
            (al_nb_pac == 0) * (statut_occupation_logement != 3) * not_(proprietaire_proche_famille) *
            no_parent_etudiant * aide_logement_montant
            )

class als_etudiant(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Famille
    label = u"Allocation logement sociale (étudiante)"
    url = u"https://www.caf.fr/actualites/2012/etudiants-tout-savoir-sur-les-aides-au-logement"
    definition_period = MONTH

    def function(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        proprietaire_proche_famille = famille('proprietaire_proche_famille', period)

        etudiant = famille.members('etudiant', period)
        parent_etudiant = famille.any(etudiant, role = Famille.PARENT)

        return (
            (al_nb_pac == 0) * (statut_occupation_logement != 3) * not_(proprietaire_proche_famille) *
            parent_etudiant * aide_logement_montant
        )

class als(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Famille
    label = u"Allocation logement sociale"
    url = u"http://vosdroits.service-public.fr/particuliers/F1280.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        als_non_etudiant = simulation.calculate('als_non_etudiant', period)
        als_etudiant = simulation.calculate('als_etudiant', period)
        result = (als_non_etudiant + als_etudiant)

        return result


class apl(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Famille
    label = u" Aide personnalisée au logement"
    # (réservée aux logements conventionné, surtout des HLM, et financé par le fonds national de l'habitation)"
    url = u"http://vosdroits.service-public.fr/particuliers/F12006.xhtml",
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def function(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)

        return aide_logement_montant * (statut_occupation_logement == 3)


class aide_logement_non_calculable(Variable):
    column = EnumCol(
        enum = Enum([
            u"",
            u"primo_accedant",
            u"locataire_foyer"
            ]),
        default = 0
        )
    entity = Famille
    label = u"Aide au logement non calculable"
    definition_period = MONTH

    def function(famille, period):
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)

        return (statut_occupation_logement == 1) * 1 + (statut_occupation_logement == 7) * 2


class aide_logement(Variable):
    column = FloatCol
    entity = Famille
    label = u"Aide au logement (tout type)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        apl = simulation.calculate('apl', period)
        als = simulation.calculate('als', period)
        alf = simulation.calculate('alf', period)

        return max_(max_(apl, als), alf)


class crds_logement(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Famille
    label = u"CRDS des allocations logement"
    url = u"http://vosdroits.service-public.fr/particuliers/F17585.xhtml"
    definition_period = MONTH

    def function(self, simulation, period):
        aide_logement_montant_brut = simulation.calculate('aide_logement_montant_brut', period)
        crds = simulation.legislation_at(period.start).prestations.prestations_familiales.af.crds
        return -aide_logement_montant_brut * crds


class zone_apl(Variable):
    column = EnumCol(
        enum = Enum([
            u"Non renseigné",
            u"Zone 1",
            u"Zone 2",
            u"Zone 3",
            ]),
        default = 2
        )
    entity = Menage
    label = u"Zone APL"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def function(self, simulation, period):
        '''
        Retrouve la zone APL (aide personnalisée au logement) de la commune
        en fonction du depcom (code INSEE)
        '''
        depcom = simulation.calculate('depcom', period)

        preload_zone_apl()
        default_value = 2
        return fromiter(
            (
                zone_apl_by_depcom.get(depcom_cell, default_value)
                for depcom_cell in depcom
                ),
            dtype = int16,
            )


def preload_zone_apl():
    global zone_apl_by_depcom
    if zone_apl_by_depcom is None:
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/apl/20110914_zonage.csv',
                ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            zone_apl_by_depcom = {
                # Keep only first char of Zonage column because of 1bis value considered equivalent to 1.
                row['CODGEO']: int(row['Zonage'][0])
                for row in csv_reader
                }
        # Add subcommunes (arrondissements and communes associées), use the same value as their parent commune.
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/apl/commune_depcom_by_subcommune_depcom.json',
                ) as json_file:
            commune_depcom_by_subcommune_depcom = json.load(json_file)
            for subcommune_depcom, commune_depcom in commune_depcom_by_subcommune_depcom.iteritems():
                zone_apl_by_depcom[subcommune_depcom] = zone_apl_by_depcom[commune_depcom]
