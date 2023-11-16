#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 12:12:19 2023

@author: raphael
"""

import pytest
from models.search_test import (
    Critere, Champ, NomCodeFiltre, NatureFiltre, DateVersionFiltre,
    Recherche, RechercheFinal, TypeRecherche, 
    Operateur, ChampsCODE, FacettesCODE, FacettesLODA
    )


        
def test_champ_valide(): 
    criteria= Critere(valeur='7', typeRecherche=TypeRecherche.EXACTE, operateur=Operateur.ET)
    field = Champ(typeChamp="VISA", criteres=[criteria], operateur=Operateur.ET)
    return field
        
def test_RechercheFinal_fond_type_champs_valide(): 
    
    criteria= Critere(valeur="7", typeRecherche="EXACTE", operateur="ET")

    #Le modèle à tester : VISA est dans ChampsLODA :
    field = Champ(typeChamp="VISA", criteres=[criteria], operateur=Operateur.ET)
    # ------------

    filtre = NomCodeFiltre(valeurs=["Code civil"])
    search = Recherche(champs=[field], filtres=[filtre])
    
    # en fonction du fond
    final = RechercheFinal(recherche=search, fond='LODA_DATE')
    
def test_RechercheFinal_fond_type_champs_non_valide(): 
        
    criteria= Critere(valeur="7", typeRecherche="EXACTE", operateur="ET")

    # Le modèle à tester : VISA n'est pas dans le ChampsCODE
    field = Champ(typeChamp="VISA", criteres=[criteria], operateur=Operateur.ET)
    # ------------
    
    filtre = NomCodeFiltre(valeurs=["Code civil"])
    search = Recherche(champs=[field], filtres=[filtre])

    # en fonction du fond :
    final = RechercheFinal(recherche=search, fond="CODE_DATE")
    
    return final

def test_RechercheFinal_fond_type_filtres_valide(): 
        
    criteria= Critere(valeur="7", typeRecherche="EXACTE", operateur="ET")
    field = Champ(typeChamp="NUM_ARTICLE", criteres=[criteria], operateur="ET")
    
    #Le modèle à tester : NomCodeFiltre autorisé pour le fond CODE
    filtre = NomCodeFiltre(valeurs=["Code civil"])
    filtre2 = DateVersionFiltre()
    # ------------
    
    search = Recherche(champs=[field], filtres=[filtre, filtre2])
    # en fonction du fond 
    final = RechercheFinal(recherche=search, fond="CODE_DATE")
    
    return final

def test_RechercheFinal_fond_type_filtres_non_valide(): 
        
    criteria= Critere(valeur="7", typeRecherche="EXACTE", operateur="ET")
    field = Champ(typeChamp="NUM_ARTICLE", criteres=[criteria], operateur=Operateur.ET)
    
    #Le modèle à tester : NomCodeFiltre non autorisé pour le fond LODA
    filtre = NomCodeFiltre(valeurs=["Code civil"])
    filtre2 = DateVersionFiltre()
    # ------------
    
    search = Recherche(champs=[field], filtres=[filtre, filtre2])
    # en fonction du fond 
    final = RechercheFinal(recherche=search, fond="LODA_DATE")
    
    return final



