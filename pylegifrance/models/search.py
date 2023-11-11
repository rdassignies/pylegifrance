#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 18:00:49 2023

@author: raphael
"""

from datetime import datetime

from models.models import * 


# Création des objets CritereDTO
critere = CritereDTO(
    typeRecherche=TypeRecherche.EXACTE,
    valeur="L36-11",
    operateur=Operateur.ET
)

# Création de l'objet ChampDTO
champ = ChampDTO(
    typeChamp=TypeChamp.NUM_ARTICLE,
    criteres=[critere],
    operateur=Operateur.ET
)

# Création des objets FiltreDTO
filtre1 = FiltreDTO(
    facette="NOM_CODE",
    valeurs=["Code des postes et des communications électroniques"]
)

filtre2 = FiltreDTO(
    facette="DATE_VERSION",
    singleDate=datetime.fromtimestamp(1514802418000 / 1000).strftime('%Y-%m-%d')
)

# Création de l'objet RechercheSpecifiqueDTO
recherche_specifique = RechercheSpecifiqueDTO(
    champs=[champ],
    filtres=[filtre1, filtre2],
    typePagination=TypePagination.ARTICLE,
    pageNumber=1,
    pageSize=10,
    sort="PERTINENCE"
)

# Création de l'objet Recherche code
recherche = Recherche(
    recherche=recherche_specifique,
    fond=Fonds.CODE_DATE
)



