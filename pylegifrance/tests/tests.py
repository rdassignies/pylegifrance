#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 12:12:19 2023

@author: raphael
"""

import pytest
from models.search_test import (
    Critere, Champ, Recherche, 
    RechercheFinal, GlobalModel, TypeRecherche, 
    Operateur, ChampsCODE)

def test_critere_valide():
    critere = Critere(valeur="test", typeRecherche=TypeRecherche.EXACT, operateur=Operateur.ET)
    assert critere.valeur == "test"

def test_critere_invalide():
    with pytest.raises(ValueError):
        Critere(valeur="test", typeRecherche="NonValide", operateur=Operateur.ET)

# Répétez pour chaque modèle avec des variations pour couvrir différents cas
