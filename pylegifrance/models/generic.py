#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:07:49 2023
Modèles génériques de l'API legifrance

@author: raphael
"""

from enum import Enum


# from pydantic import BaseModel, field_validator


# Enums génériques
class Operateur(Enum):
    """
    Opérateur entre les champs de recherche
    """
    ET = "ET"
    OU = "OU"


class TypeChamp(Enum):
    """
    Type de champ. Il est possible d'utiliser la valeur ALL pour r
    echercher dans tous les champs.
    """
    ALL = "ALL"
    TITLE = "TITLE"
    TABLE = "TABLE"
    NOR = "NOR"
    NUM = "NUM"
    ADVANCED_TEXTE_ID = "ADVANCED_TEXTE_ID"
    NUM_DELIB = "NUM_DELIB"
    NUM_DEC = "NUM_DEC"
    NUM_ARTICLE = "NUM_ARTICLE"
    ARTICLE = "ARTICLE"
    MINISTERE = "MINISTERE"
    VISA = "VISA"
    NOTICE = "NOTICE"
    VISA_NOTICE = "VISA_NOTICE"
    TRAVAUX_PREP = "TRAVAUX_PREP"
    SIGNATURE = "SIGNATURE"
    NOTA = "NOTA"
    NUM_AFFAIRE = "NUM_AFFAIRE"
    ABSTRATS = "ABSTRATS"
    RESUMES = "RESUMES"
    TEXTE = "TEXTE"
    ECLI = "ECLI"
    NUM_LOI_DEF = "NUM_LOI_DEF"
    TYPE_DECISION = "TYPE_DECISION"
    NUMERO_INTERNE = "NUMERO_INTERNE"
    REF_PUBLI = "REF_PUBLI"
    RESUME_CIRC = "RESUME_CIRC"
    TEXTE_REF = "TEXTE_REF"
    TITRE_LOI_DEF = "TITRE_LOI_DEF"
    RAISON_SOCIALE = "RAISON_SOCIALE"
    MOTS_CLES = "MOTS_CLES"
    IDCC = "IDCC"


class TypeRecherche(Enum):
    """Type de recherche effectuée
    """
    EXACTE = "EXACTE"
    UN_DES_MOTS = "UN_DES_MOTS"
    TOUS_LES_MOTS_DANS_UN_CHAMP = "TOUS_LES_MOTS_DANS_UN_CHAMP"
    AUCUN_DES_MOTS = "AUCUN_DES_MOTS"
    AUCUNE_CORRESPONDANCE_A_CETTE_EXPRESSION = "AUCUNE_CORRESPONDANCE_A_CETTE_EXPRESSION"

class Fonds(str, Enum):
    """ Liste des fonds disponibles pour la recherche
    Fonds sur lequel appliquer la recherche. Pour rechercher dans tous les
    fonds, il faut définir la valeur ALL.
    Pour les fonds LODA et CODE, il existe deux types de recherche :
    la recherche par date (_DATE) den version ou la recherche par état
    juridique (_ETAT)
    """

    JORF = "JORF"
    CNIL = "CNIL"
    CETAT = "CETAT"
    JURI = "JURI"
    JUFI = "JUFI"
    CONSTIT = "CONSTIT"
    KALI = "KALI"
    CODE_DATE = "CODE_DATE"
    CODE_ETAT = "CODE_ETAT"
    LODA_DATE = "LODA_DATE"
    LODA_ETAT = "LODA_ETAT"
    ALL = "ALL"
    CIRC = "CIRC"
    ACCO = "ACCO"

class TypeFacettes(str, Enum): 
    NOM_CODE = "NOM_CODE"
    DATE_SIGNATURE = "DATE_SIGNATURE"
    DATE_VERSION = "DATE_VERSION"
    TEXT_LEGAL_STATUS = "TEXT_LEGAL_STATUS"
    ARTICLE_LEGAL_STATUS = "ARTICLE_LEGAL_STATUS"
    NATURE = "NATURE"
    NOR = "NOR"


class CodeNom(str, Enum):
    CC = "Code civil"
    CDC = "Code des communes"
    CDDDA = "Code de déontologie des architectes"
    CDJA = "Code de justice administrative"
    CDJM = "Code de justice militaire (nouveau)"
    CDSEDF = "Code de l'action sociale et des familles"
    CD = "Code de l'énergie"
    CDEDSDÉEDD = "Code de l'entrée et du séjour des étrangers et du droit d'asile"
    CDPCP = "Code de l'expropriation pour cause d'utilité publique"
    CDJ = "Code de l'organisation judiciaire"
    CDLCP = "Code de la commande publique"
    CDLC = "Code de la consommation"
    CDLCED = "Code de la construction et de l'habitation"
    CDLD = "Code de la défense"
    CDLFEDS = "Code de la famille et de l'aide sociale"
    CDLJPDM = "Code de la justice pénale des mineurs"
    CDLLDLMMEDNDM = "Code de la Légion d'honneur, de la Médaille militaire et de l'ordre national du Mérite"
    CDLM = "Code de la mutualité"
    CDLPI = "Code de la propriété intellectuelle"
    CDLR = "Code de la route"
    CDLSP = "Code de la santé publique"
    CDLSI = "Code de la sécurité intérieure"
    CDLSS = "Code de la sécurité sociale"
    CDLVR = "Code de la voirie routière"
    CDPC = "Code des procédures civiles d'exécution"
    CDPP = "Code de procédure pénale"
    CDA = "Code des assurances"
    CDCDL = "Code des communes de la Nouvelle-Calédonie"
    CDD = "Code des douanes"
    CDDDM = "Code des douanes de Mayotte"
    CDISLBES = "Code des impositions sur les biens et services"
    CDIMEDM = "Code des instruments monétaires et des médailles"
    CDJF = "Code des juridictions financières"
    CDPCEMDR = "Code des pensions civiles et militaires de retraite"
    CDPDRDMFDDPODP = "Code des pensions de retraite des marins français du commerce, de pêche ou de plaisance"
    CDPMEDVDG = "Code des pensions militaires d'invalidité et des victimes de guerre"
    CDPM = "Code des ports maritimes"
    CDPEDCÉ = "Code des postes et des communications électroniques"
    CDRELPE = "Code des relations entre le public et l'administration"
    CDT = "Code du travail"
    CDEPDLMM = "Code disciplinaire et pénal de la marine marchande"
    CDCEDA = "Code du cinéma et de l'image animée"
    CDDD = "Code du domaine de l'Etat"
    CDDDEDCPAÀLCTDM = "Code du domaine de l'Etat et des collectivités publiques applicable à la collectivité territoriale de Mayotte"
    CDDPFEDLNI = "Code du domaine public fluvial et de la navigation intérieure"
    CDP = "Code du patrimoine"
    CDSN = "Code du service national"
    CDS = "Code du sport"
    CDTM = "Code du travail maritime"
    CF = "Code forestier (nouveau)"
    CGDLFP = "Code général de la fonction publique"
    CGDLPDPP = "Code général de la propriété des personnes publiques"
    CGDCT = "Code général des collectivités territoriales"
    CGDI = "Code général des impôts"
    CGDAI = "Code général des impôts, annexe IV"
    CM = "Code minier (nouveau)"
    CMEF = "Code monétaire et financier"
    CP = "Code pénitentiaire"
    CR = "Code rural (ancien)"
    CREDLPM = "Code rural et de la pêche maritime"
    CÉ = "Code électoral"
    LDPF = "Livre des procédures fiscales"
    """
    CASF = "Code de l'action sociale et des familles"
    CCIV = "Code civil"
    CPRCIV = "Code de procédure civile"
    CCOM = "Code de commerce"
    CTRAV = "Code du travail"
    CPI = "Code de la propriété intellectuelle"
    CPEN = "Code pénal"
    CPP = "Code de procédure pénale"
    CASSUR = "Code des assurances"
    CCONSO = "Code de la consommation"
    CSI = "Code de la sécurité intérieure"
    CSP = "Code de la santé publique"
    CSS = "Code de la sécurité sociale"
    CESEDA = "Code de l'entrée et du séjour des étrangers et du droit d'asile"
    CGCT = "Code général des collectivités territoriales"
    CPCE = "Code des postes et des communications électroniques"
    CENV = "Code de l'environnement"
    CJA = "Code de justice administrative"
    """