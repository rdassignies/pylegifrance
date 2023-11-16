#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:07:49 2023

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
    NATURE = "NATURE"
    NOR = "NOR"


class CodeNom(str, Enum):
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
    