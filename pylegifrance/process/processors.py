#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:57:20 2023
Fonctions qui traite les résultats renvoyés par l'API legifrance
@author: Raphaël d'Assignies
"""

from typing import Union, Dict, Any
import json
import logging

from pylegifrance.models.consult import GetArticle, LegiPart

logger = logging.getLogger(__name__)


def search_response_DTO(results: Union[Dict[str, Any], str]):
    """
    Cette fonction extrait les données de SearchResponseDTO model
    (RechercheFinal).

    Args:
        results (Dict): Dict de résultats (clé 'results') renvoyé
        par l'API Legifrance

    Returns:
        extracted_data (List): renvoir une liste (text, section, article).
    """

    if isinstance(results, str):
        try:
            # Essayer de parser data en tant que JSON
            results = json.loads(results)
        except json.JSONDecodeError:
            raise ValueError("results must be a valid JSON.")

    if not isinstance(results, dict):
        raise TypeError("results must be a valid dict")

    logger.info(f"Nombre de résultats trouvés: {results.get('totalResultNumber', 0)}")
    logger.debug(f"Facets : {results.get('facets', {})}")

    def get_with_default(dictionary, key, default=""):
        value = dictionary.get(key)
        return value if value is not None else default

    extracted_data = []

    # Fonction récursive pour parcourir les éléments
    def extract_recursive(element):
        # Extraire les données de 'titles' si elles existent
        if "titles" in element:
            for title in element["titles"]:
                extracted_data.append(
                    {
                        "title_id": get_with_default(title, "id"),
                        "title_cid": get_with_default(title, "cid"),
                        "title": get_with_default(title, "title"),
                    }
                )

        # Extraire les données de 'sections' si elles existent
        if "sections" in element:
            for section in element["sections"]:
                extracted_data.append(
                    {
                        "section_id": get_with_default(section, "id"),
                        "title": (section, "title"),
                    }
                )
                # Appel récursif pour les extracts dans les sections
                if "extracts" in section:
                    for extract in section["extracts"]:
                        extracted_data.append(
                            {
                                "extract_id": get_with_default(extract, "id"),
                                "num": get_with_default(extract, "num"),
                                "legal_status": get_with_default(
                                    extract, "legalStatus"
                                ),
                                "date_version": get_with_default(
                                    extract, "dateVersion"
                                ),
                                "title": get_with_default(extract, "title"),
                                "values": get_with_default(extract, "values"),
                            }
                        )

    # Appel initial sur les résultats
    if (
        isinstance(results, dict)
        and "results" in results
        and isinstance(results["results"], list)
    ):
        for result in results["results"]:
            extract_recursive(result)

    return extracted_data


def get_text_id(data):
    """
    Cette fonction extrait le ou les identifiant d'un texte (LEGITEXT)
    des résultats d'une recherche.

    Args:
        data (Dict): Résultat de la recherche de l'API Legifrance
        (ExtractSearchResult from search_response_DTO).

    Raises:
        GetTextIdError: Renvoi une exception si aucun LEGITEXT trouvé

    Returns:
        LegiPart(BaseModel): Les ids LEGITEXT.
    """
    # Logging processing information
    logger.debug("get_text_id: RETRIEVING LEGITEXT --------")
    text_ids = []
    for item in data:
        if "title_id" in item and item["title_id"].startswith("LEGITEXT"):
            text_ids.append(LegiPart(textId=item["title_id"]))

    logger.debug(f"Size of data containing LEGITEXT: {len(text_ids)}")

    if not text_ids:
        raise GetTextIdError(
            "La liste GetText est vide !"
            "- Pas d'identifiant LEGITEXT trouvé."
            "Vérifier vos critères de recherche."
        )
    return text_ids


def get_article_id(data):
    """
    Cette fonction extrait les identifiants des articles (LEGIARTI)
    des résultats d'une recherche.

    Args:
        data (Dict): Résultat de la recherche de l'API Legifrance
        (ExtractSearchResult from search_response_DTO).

    Raises:
        GetArticleIdError: Renvoi une exception si aucun LEGIARTI trouvé

    Returns:
        LegiPart(BaseModel): Les ids LEGIARTI.
    """

    # Logging processing information
    logger.debug("get_article_id: RETRIEVING LEGIARTI ---------")

    article_ids = []
    for item in data:
        if "extract_id" in item and item["extract_id"].startswith("LEGIARTI"):
            article_ids.append(GetArticle(id=item["extract_id"]))

    logger.debug(f"Size of data containing LEGIARTI: {len(article_ids)}")

    if not article_ids:
        raise GetArticleIdError(
            "La liste GetArticle est vide !"
            "- Pas d'identifiant LEGIARTI trouvé."
            "Vérifier vos critères de recherche."
        )

    return article_ids


class GetArticleIdError(Exception):
    """Lève une exception si LEGIARTI list est vide."""

    pass


class GetTextIdError(Exception):
    """Lève une exception si LEGITEXT list est vide."""

    pass
