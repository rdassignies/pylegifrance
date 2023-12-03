#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 19:17:02 2023
Atelier de création des fonctions de recherche dans les différents fonds
legifrance et autres.
@author: Raphaël d'Assignies
"""
import logging
import os
from typing import List
from importlib import resources

from pylegifrance.pipeline.pipeline import (
    Pipeline, CallApiStep, ExtractSearchResult,
    GetArticleId, GetTextId, Formatters
    )
from pylegifrance.client.api import LegiHandler
from pylegifrance.models.search import (
    Critere, Champ, NomCodeFiltre, NatureFiltre, DateVersionFiltre,
    EtatTextFiltre, EtatArticleFiltre, NatureFiltre, DatesPeriod, 
    DateSignatureFiltre, Fond, Recherche, RechercheFinal, TypeRecherche,
    Operateur, ChampsCODE, FacettesCODE, FacettesLODA
    )
import yaml

from importlib import resources

with resources.open_text('pylegifrance', 'config.yaml') as file:
    config = yaml.safe_load(file)

logging_level = config['logging']['level']
logging.basicConfig(level=logging_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

def recherche_CODE(
                   code_name: str,
                   search: str = '',
                   champ: str = 'NUM_ARTICLE',
                   type_recherche: str = "EXACTE",
                   fond: str = "CODE_DATE",
                   formatter: bool = False,
                   page_number: int = 1,
                   page_size: int = 10,
                   *args
                   ):
    """Recherche dans le fond CODE (CODE_DATE, CODE_ETAT) un article par son numéro, 
    un terme de recherche ou un code dans son intégralité.

    Cette fonction ne récupère que les codes en vigueur à la date actuelle. 
    Par défaut, la facette "DATE_VERSION" est définie sur la date du jour, quel que soit 
    le fond cible (CODE_DATE ou CODE_ETAT).

    Attention : Il est de la responsabilité de l'utilisateur de vérifier 
    que les informations renvoyées par l'API sont pertinentes et actuelles.

    Certains paramètres comme "sort" ou "typepagination" ne sont pas encore accessibles 
    (voir models.search pour plus de détails).

    Instructions : 
    - Pour rechercher un code en intégralité : code_name="Code civil"
    - Pour rechercher l'article 7 du Code civil : search="7", code_name="Code civil"
    - Pour rechercher le mot "sûreté" dans le Code civil : search="sureté", 
      code_name="Code civil", champ="ARTICLE"

    Args:
        code_name (str): Nom du Code (ex. "Code civil").
        search (str, optional): Terme recherché dans un champ spécifique du code.
        champ (str, optional): Type de champ de recherche, par défaut 'NUM_ARTICLE'. 
                               valeurs possibles : 'ALL', 'NUM_ARTICLE', 'TITLE', 'TABLE'.
        type_recherche (str, optional): Type de recherche. Par défaut est "EXACTE".
                               valeurs possibles : UN_DES_MOTS, EXACTE, TOUS_LES_MOTS_DANS_UN_CHAMP, 
                               AUCUN_DES_MOTS, AUCUNE_CORRESPONDANCE_A_CETTE_EXPRESSION
        fond (str, optional): Type de fond parmi CODE_DATE ou CODE_ETAT. Par défaut est "CODE_DATE".
        nature (list): sous-ens. du fond LODA (LOI, ORDONNANCE, DECRET, ARRETE). Par défaut tous les textes du fond. 
        formatter (bool, optional): Active le formatage dynamique du résultat final.
        page_number (int, optional): Numéro de la page de résultat. Par défaut à 1.
        page_size (int, optional): Nombre de résultats par page. Par défaut à 10 (max 100).
        *args: Arguments additionnels non implémentés pour le moment.

    Returns:
        Dict: Soit un code en intégralité soit un ou plusieurs articles correspondant à la recherche.
    """

    # Initialisation du client (singleton)
    client = LegiHandler()
    client.set_api_keys()
        
    # TODO: ajouter la possibilité de rapatrier un code dans son intégralité si search=None
    # Création des critères de recherche
    
    criteres = [Critere(valeur=search,
                        typeRecherche=type_recherche,
                        operateur="ET")]

    # Création des champs de recherche
    field = Champ(typeChamp=champ, criteres=criteres, operateur="ET")

    if args:
        print("ATTENTION : Traitement de *args pas encore implémenté.")
        # TODO: Implémenter le traitement pour *args permettant des requêtes plus flexibles

    # Création des filtres
    filtre_code = NomCodeFiltre(valeurs=[code_name])
    filtre_date = DateVersionFiltre()

    # Construction des paramètres de la recherche
    recherche = Recherche(champs=[field],
                          filtres=[filtre_code, filtre_date],
                          pageNumber=page_number,
                          pageSize=page_size
                          )

    # Construction de la requête finale (payload)
    
    # Astuce qui permet de valider le fond recherché 
    fond_cible=Fond(fond=fond)
    initial_data = RechercheFinal(recherche=recherche, fond=fond)

    logger.debug("---------- Payload -------------")
    logger.debug(initial_data.model_dump(mode='json'))

    # Initialisation des étapes du pipeline
    pipeline_steps = [
        CallApiStep(client),
        ExtractSearchResult(),
        GetArticleId(),
        CallApiStep(client),
    ]
    # Sisearch=='' récupérer le textid à la place
    if not search:
        pipeline_steps[2] = GetTextId()

    # Ajoute un formatter si demandé
    if formatter:
        pipeline_steps.append(Formatters())

    # Instanciation de Pipeline
    pl = Pipeline(pipeline_steps)

    # Exécution du pipeline
    result = pl.execute(data=initial_data)

    return result


def recherche_LODA(
                   text_id: str = '',
                   search: str = None,
                   champ: str = 'NUM_ARTICLE',
                   type_recherche: str = "EXACTE",
                   fond: str = "LODA_DATE",
                   nature: List = ["LOI", "ORDONNANCE", "DECRET", "ARRETE"],
                   date_signature: List = None,
                   formatter: bool = False,
                   page_number: int = 1,
                   page_size: int = 10,
                   *args
                   ):
    """ Recherche dans le fond LODA (LODA_DATE, LODA_ETAT) un texte par son numéro, 
    un article dans un texte spécifique, ou un terme de recherche dans les champs d'un texte.

    Cette fonction ne récupère que les textes en vigueur à la date actuelle. 
    Par défaut, la facette "DATE_VERSION" est définie sur la date du jour, et les facettes 
    "TEXT_LEGAL_STATUS" et "ARTICLE_LEGAL_STATUTS" sont définies sur "VIGEUR", 
    quel que soit le fond cible (LODA_DATE ou LODA_ETAT).

    Attention : Il est de la responsabilité de l'utilisateur de vérifier 
    que les informations renvoyées par l'API sont pertinentes et actuelles.

    Certains paramètres comme "sort" ou "typepagination" ne sont pas encore accessibles 
    (voir models.search pour plus de détails).

    Instructions : 
    - Pour rechercher un texte intégral par son numéro : text="78-17"
    - Pour rechercher un article dans un texte : text="78-17", search="9"
    - Pour rechercher un terme dans un texte spécifique dans tous les champs :
      text="78-17", search="autorité", champ="ALL"

    Args:
        text (str): Numéro de texte (ex. "78-17").
        search (str, optional): Terme(s) de recherche. Par défaut est None.
        champ (str, optional): Type de champ de recherche, par défaut 'NUM_ARTICLE'. 
                               valeurs possibles : 'ALL', 'TITLE', 'NOR', 'NUM_ARTICLE', 
                               'NUM', 'ARTICLE', 'VISA', 'NOTICE', 'VISA_NOTICE', 
                               'TRAVAUX_PREP', 'SIGNATURE', 'NOTA' par état ou date.
        type_recherche (str, optional): Type de recherche. Par défaut est "EXACTE".
                               valeurs possibles : UN_DES_MOTS, EXACTE, TOUS_LES_MOTS_DANS_UN_CHAMP, 
                               AUCUN_DES_MOTS, AUCUNE_CORRESPONDANCE_A_CETTE_EXPRESSION
        fond (str, optional): Type de fond parmi LODA_DATE ou LODA_ETAT. Par défaut est "LODA_DATE".
        nature (list) : Type de texte recherché parmi LOI, ORD., DECRET, ARRETE
        date_signature(list) : date (start et end) de signature au format "YYYY-MM-DD"
        formatter (bool, optional): Active le formatage dynamique du résultat final.
        page_number (int, optional): Numéro de la page de résultat. Par défaut à 1.
        page_size (int, optional): Nombre de résultats par page. Par défaut à 10 (max 100).
        *args: Arguments additionnels non implémentés pour le moment.

    Returns:
        Dict: Soit un texte intégral soit un ou plusieurs articles correspondant à la recherche.
    """

    # Initialisation du client (singleton)
    client = LegiHandler()
    client.set_api_keys()

    # Création des critères de recherche
    critere_text = [Critere(valeur=text_id,
                            typeRecherche="EXACTE",
                            operateur="ET")]
    # Création des champs de recherche
    fields = [Champ(typeChamp="NUM",
                    criteres=critere_text,
                    operateur="ET")]

    # Création de champs supplémentaires si search non vide

    if search:
        critere_art = [Critere(valeur=search,
                               typeRecherche="EXACTE",
                               operateur="ET")]
        fields.append(Champ(typeChamp=champ,
                            criteres=critere_art,
                            operateur="ET"))

    if args:
        print("ATTENTION : Traitement de *args pas encore implémenté.")
        # TODO: Implémenter le traitement pour args pemettant des requêtes plus flexibles

    # Création des filtres
    filtre_date = DateVersionFiltre()
    filtre_etat_text = EtatTextFiltre()
    filtre_etat_art = EtatArticleFiltre()
    filtre_nature = NatureFiltre(valeurs=nature)
    filtres = [filtre_etat_text,
               filtre_etat_art,
               filtre_date,
               filtre_nature]

    if date_signature:
        filtre_date_sig = DateSignatureFiltre(
            dates=DatesPeriod(start=date_signature[0], end=date_signature[1])
            )
        filtres.append(filtre_date_sig)

    # Construction des paramètres de la recherche
    recherche = Recherche(champs=fields,
                          filtres=filtres,
                          pageNumber=page_number,
                          pageSize=page_size
                         )

    # Construction de la requête finale (payload)

    # Astuce qui permet de valider le fond recherché = lève erreur si pas valide
    fond_cible = Fond(fond=fond)

    initial_data = RechercheFinal(recherche=recherche, fond=fond)

    logger.debug("---------- Payload -------------")
    logger.debug(initial_data.model_dump(mode='json'))

    # Initialisation des étapes du pipeline
    pipeline_steps = [
        CallApiStep(client),
        ExtractSearchResult(),
        GetArticleId(),
        CallApiStep(client),
    ]

    # Trouve le textid si pas de recherche par mot clé
    if not search:
        pipeline_steps[2] = GetTextId()

    # Ajoute un formatter si True
    if formatter:
        pipeline_steps.append(Formatters())

    # Instanciation de Pipeline
    pl = Pipeline(pipeline_steps)

    # Exécution du pipeline
    result = pl.execute(data=initial_data, data_type='')

    return result


def recherche_JURI(
                    search: str = None,
                    champ: str = 'ALL',
                    type_recherche: str = "EXACTE",
                    fond: str = "JURI",
                    formatter: bool = False,
                    page_number: int = 1,
                    page_size: int = 10,
                    *args):
    # TODO: à implémenter

    # Initialisation du client (singleton)
    client = LegiHandler()
    client.set_api_keys()

    # Création des critères de recherche
    critere = [Critere(valeur=search,
                       typeRecherche="EXACTE",
                       operateur="ET")]
    
    fields = [Champ(typeChamp=champ,
                    criteres=critere,
                    operateur="ET")]

    # Construction des paramètres de la recherche
    recherche = Recherche(champs=fields,
                          filtres=[],
                          pageNumber=page_number,
                          pageSize=page_size
                         )

    # Astuce qui permet de valider le fond recherché 
    fond_cible = Fond(fond=fond)

    initial_data = RechercheFinal(recherche=recherche, fond=fond)

    logger.debug("---------- Payload -------------")
    logger.debug(initial_data.model_dump(mode='json'))

    # Initialisation des étapes du pipeline
    pipeline_steps = [
        CallApiStep(client)
    ]

    # Ajoute un formatter si True
    if formatter:
        pipeline_steps.append(Formatters())

    # Instanciation de Pipeline
    pl = Pipeline(pipeline_steps)

    # Exécution du pipeline
    result = pl.execute(data=initial_data, data_type='')

    return result
    

def recherche_CETAT():
    # TODO: à implémenter
    pass
