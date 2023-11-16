#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 19:17:02 2023

@author: Raphaël d'Assignies
"""
from typing import Union, List
import logging

from pipeline.pipeline import (
    Pipeline, CallApiStep, ExtractSearchResult, 
    GetArticleId, GetTextId, Formatters
    )
from api import LegiHandler

from models.search import (
    Critere, Champ, NomCodeFiltre, NatureFiltre, DateVersionFiltre, EtatFiltre,
    Recherche, RechercheFinal, TypeRecherche, 
    Operateur, ChampsCODE, FacettesCODE, FacettesLODA
    )

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def recherche_CODE(client:LegiHandler=None, 
                   nom_code: str=None, 
                   search: str = None,
                   champ: str = 'NUM_ARTICLE',
                   type_recherche: str = "EXACTE", 
                   fond: str="CODE_DATE",
                   formatter:bool =False, 
                   page_number = 1,
                   page_size = 10, 
                   *args
                   ):

   
    
    # TODO: ajouter la possibilité de rapatrier un code dans son intégralité si search=None
    # Création des critères de recherche    
    criteres = [Critere(valeur=search, typeRecherche=type_recherche, operateur="ET")]

    # Création des champs de recherche
    field = Champ(typeChamp=champ, criteres=criteres, operateur="ET")

    if args:
        print("ATTENTION : Traitement de *args pas encore implémenté.")
        # TODO: Implémenter le traitement pour *args permettant des requêtes plus flexibles

    # Création des filtres
    filtre_code = NomCodeFiltre(valeurs=[nom_code])
    filtre_date = DateVersionFiltre()

    # Construction des paramètres de la recherche
    search = Recherche(champs=[field], 
                       filtres=[filtre_code, filtre_date], 
                       pageNumber=page_number, 
                       pageSize=page_size
                       )

    # Construction de la requête finale (payload)
    initial_data = RechercheFinal(recherche=search, fond=fond)
    
    logger.debug(f"---------- Payload -------------")
    logger.debug(initial_data.model_dump(mode='json'))
    
    # Initialisation des étapes du pipeline
    pipeline_steps = [
        CallApiStep(client),
        ExtractSearchResult(),
        GetArticleId(),
        CallApiStep(client), 
    ]
    
    # Ajoute un formatter si True
    if formatter: 
       pipeline_steps.append(Formatters())

    # Instanciation de Pipeline
    pl = Pipeline(pipeline_steps)
    
    # exécution du pipeline
    result = pl.execute(data=initial_data)

    return result

def recherche_LODA(client: LegiHandler,
                   text: str,
                   article: str = None,
                   type_recherche: str = "EXACTE",
                   fond: str = "LODA_DATE",
                   page_number = 1, # A mettre dans une autre version
                   page_size = 10, 
                   *args

    # Création des critères de recherche
    critere_text = [Critere(valeur=text, 
                        typeRecherche="EXACTE", 
                        operateur="ET")]
    # Création des champs de recherche
    fields = [Champ(typeChamp="NUM", 
                   criteres=critere_text, 
                   operateur="ET")]

    # Création de champs supplémentaires si article 
    if article: 
       critere_art = [Critere(valeur=article,
                              typeRecherche="EXACTE",
                              operateur="ET")]

       fields.append(Champ(typeChamp="NUM_ARTICLE",
                           criteres=critere_art,
                           operateur="ET"))


    if args:
        print("ATTENTION : Traitement de *args pas encore implémenté.")
        # TODO: Implémenter le traitement pour args pemettant des requêtes plus flexibles

    # Création des filtres
    filtre_date = DateVersionFiltre()
    filtre_etat = EtatFiltre()

    # Construction des paramètres de la recherche
    search = Recherche(champs=fields, 
                       filtres=[filtre_etat, filtre_date], 
                       pageNumber=page_number, 
                       pageSize=page_size
                       )

    # Construction de la requête finale (payload)
    initial_data = RechercheFinal(recherche=search, fond=fond)

    logger.debug(f"---------- Payload -------------")
    logger.debug(initial_data.model_dump(mode='json'))

    # Initialisation des étapes du pipeline
    pipeline_steps = [
        CallApiStep(client),
        ExtractSearchResult(),
        GetTextId(),
        CallApiStep(client), 
        Formatters()
    ]

    # Change l'étape 3 si c'est un article qui est recherché
    if article:
        pipeline_steps[2] = GetArticleId()

    # Instanciation de Pipeline
    pl = Pipeline(pipeline_steps)

    # Exécution du pipeline
    result = pl.execute(data=initial_data, data_type='')

    return result

def recherche_JURI():
    # TODDO : à implémenter
    pass
