#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 19:17:02 2023
Atelier de création des fonctions de recherche dans les différents fonds
legifrance et autres.
@author: Raphaël d'Assignies
"""

import logging
from typing import List

from dotenv import load_dotenv

from pylegifrance.pipeline.pipeline import (
    Pipeline,
    PipelineStep,
    CallApiStep,
    ExtractSearchResult,
    GetArticleId,
    GetTextId,
    Formatters,
)
from pylegifrance.client import LegifranceClient
from pylegifrance.config import ApiConfig
from pylegifrance.models.search import (
    Critere,
    Champ,
    NomCodeFiltre,
    DateVersionFiltre,
    Recherche,
    RechercheFinal,
)
from pylegifrance.models.constants import (
    Fond,
    TypeRecherche,
    Operateur,
    TypeChamp,
)

load_dotenv()

logger = logging.getLogger(__name__)


def recherche_code(
    code_name: str,
    search: str | None = None,
    champ: str = "NUM_ARTICLE",
    type_recherche: TypeRecherche = TypeRecherche.EXACTE,
    fond: str | Fond = Fond.CODE_DATE,
    formatter: bool = False,
    page_number: int = 1,
    page_size: int = 10,
    *args,
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
                               Si None, récupère le code dans son intégralité.
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
    config = ApiConfig.from_env()
    client = LegifranceClient(config=config)

    # Création des critères de recherche et des champs de recherche
    if search:
        criteres = [
            Critere(valeur=search, typeRecherche=type_recherche, operateur=Operateur.ET)
        ]
        field = Champ(
            typeChamp=TypeChamp(champ), criteres=criteres, operateur=Operateur.ET
        )
    else:
        # When search is None, use a search criterion that will match all articles
        # Using a space with the TITLE field and EXACTE type to retrieve the entire code
        criteres = [
            Critere(
                valeur=" ", typeRecherche=TypeRecherche.EXACTE, operateur=Operateur.ET
            )
        ]
        field = Champ(
            typeChamp=TypeChamp("TITLE"), criteres=criteres, operateur=Operateur.ET
        )

    champs = [field]

    if args:
        print("ATTENTION : Traitement de *args pas encore implémenté.")
        # TODO: Implémenter le traitement pour *args permettant des requêtes plus flexibles

    # Création des filtres
    filtre_code = NomCodeFiltre(valeurs=[code_name])
    filtre_date = DateVersionFiltre()

    # Construction des paramètres de la recherche
    recherche = Recherche(
        champs=champs,
        filtres=[filtre_code, filtre_date],
        pageNumber=page_number,
        pageSize=page_size,
    )

    # Construction de la requête finale (payload)

    try:
        # Convert string fond to Fonds enum
        fonds_enum = Fond(fond)
        initial_data = RechercheFinal(recherche=recherche, fond=fonds_enum)

        logger.debug("---------- Payload -------------")
        logger.debug(initial_data.model_dump(mode="json"))
    except Exception as e:
        logger.error(f"Error creating search request: {e}")
        return {"error": str(e)}

    # Initialisation des étapes du pipeline
    pipeline_steps: List[PipelineStep] = [
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
