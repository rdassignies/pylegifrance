#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 10:25:24 2023

@author: raphael
"""

# Liste des phrases fournies
phrases = [
    "Code civil", "Code de commerce", "Code de déontologie des architectes",
    "Code de justice administrative", "Code de justice militaire (nouveau)",
    "Code de l'action sociale et des familles", "Code de l'artisanat",
    "Code de l'aviation civile", "Code de l'entrée et du séjour des étrangers et du droit d'asile",
    "Code de l'environnement", "Code de l'expropriation pour cause d'utilité publique",
    "Code de l'organisation judiciaire", "Code de l'urbanisme", "Code de l'éducation",
    "Code de l'énergie", "Code de la commande publique", "Code de la consommation",
    "Code de la construction et de l'habitation", "Code de la défense",
    "Code de la famille et de l'aide sociale", "Code de la justice pénale des mineurs",
    "Code de la Légion d'honneur, de la Médaille militaire et de l'ordre national du Mérite",
    "Code de la mutualité", "Code de la propriété intellectuelle", "Code de la recherche",
    "Code de la route", "Code de la santé publique", "Code de la sécurité intérieure",
    "Code de la sécurité sociale", "Code de la voirie routière", "Code de procédure civile",
    "Code de procédure pénale", "Code des assurances", "Code des communes",
    "Code des communes de la Nouvelle-Calédonie", "Code des douanes", "Code des douanes de Mayotte",
    "Code des impositions sur les biens et services", "Code des instruments monétaires et des médailles",
    "Code des juridictions financières", "Code des pensions civiles et militaires de retraite",
    "Code des pensions de retraite des marins français du commerce, de pêche ou de plaisance",
    "Code des pensions militaires d'invalidité et des victimes de guerre", "Code des ports maritimes",
    "Code des postes et des communications électroniques", "Code des procédures civiles d'exécution",
    "Code des relations entre le public et l'administration", "Code des transports",
    "Code disciplinaire et pénal de la marine marchande", "Code du cinéma et de l'image animée",
    "Code du domaine de l'Etat", "Code du domaine de l'Etat et des collectivités publiques applicable à la collectivité territoriale de Mayotte",
    "Code du domaine public fluvial et de la navigation intérieure", "Code du patrimoine",
    "Code du service national", "Code du sport", "Code du tourisme", "Code du travail",
    "Code du travail maritime", "Code forestier (nouveau)", "Code général de la fonction publique",
    "Code général de la propriété des personnes publiques", "Code général des collectivités territoriales",
    "Code général des impôts", "Code général des impôts, annexe I", "Code général des impôts, annexe II",
    "Code général des impôts, annexe III", "Code général des impôts, annexe IV",
    "Code minier", "Code minier (nouveau)", "Code monétaire et financier",
    "Code pénal", "Code pénitentiaire", "Code rural (ancien)", "Code rural et de la pêche maritime",
    "Code électoral", "Livre des procédures fiscales"
]

# Fonction pour créer les acronymes
def create_acronym(phrase):
    words = phrase.split()
    return ''.join(word[0].upper() for word in words if word.isalpha())

# Création de la liste des acronymes
codes = {create_acronym(phrase): phrase for phrase in phrases}

codes

from enum import Enum

def creer_enum_a_partir_dictionnaire(dictionnaire):
    """Crée une énumération à partir des clés d'un dictionnaire."""
    return Enum('MonEnum', {cle: cle for cle in dictionnaire.keys()})

mon_enum = creer_enum_a_partir_dictionnaire(codes)
