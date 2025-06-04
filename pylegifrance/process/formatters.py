#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:57:20 2023
Fonctions qui formatte les sorties d'une recherche en ne sélectionnant
que les clés choisie. Le paramètre de recherche doit être à formatter='True'
@author: Raphaël d'Assignies

"""

from typing import List, Dict, Any, Sequence

from pylegifrance.config import ARTICLE_KEYS, ROOT_KEYS, SECTION_KEYS


def process_section(
    section_data: Dict[str, Any],
    section_keys: Sequence[str],
    article_keys: Sequence[str],
) -> Dict[str, Any]:
    """
    Traite récursivement les sections et articles d'un texte juridique.

    Args:
        section_data (Dict[str, Any]): Données de la section à traiter
        section_keys (Sequence[str]): Liste des clés à extraire pour les sections
        article_keys (Sequence[str]): Liste des clés à extraire pour les articles

    Returns:
        Dict[str, Any]: Section formatée avec ses articles et sous-sections
    """
    section_result = {}

    # Extraire les données des articles dans la section
    if "articles" in section_data:
        section_result["articles"] = [
            {key: article[key] for key in article_keys if key in article}
            for article in section_data["articles"]
        ]

    # Extraire les données de la section elle-même
    section_result["section_data"] = {
        key: section_data[key] for key in section_keys if key in section_data
    }

    # Traiter les sous-sections récursivement
    if "sections" in section_data:
        section_result["subsections"] = [
            process_section(subsection, section_keys, article_keys)
            for subsection in section_data["sections"]
        ]

    return section_result


def formate_article_single(
    item: Dict[str, Any], article_keys: Sequence[str]
) -> Dict[str, Any]:
    """
    Formate un article individuel en extrayant les clés spécifiées.

    Args:
        item (Dict[str, Any]): Dictionnaire contenant les données de l'article
        article_keys (Sequence[str]): Liste des clés à extraire

    Returns:
        Dict[str, Any]: Article formaté avec les clés spécifiées
    """
    simplified_dict = {}
    article = item.get("article", {})

    for key in article_keys:
        simplified_dict[key] = article.get(key)

    if simplified_dict.get("cid"):
        simplified_dict["url"] = (
            f"https://www.legifrance.gouv.fr/codes/article_lc/{simplified_dict['cid']}"
        )

    return simplified_dict


def normalize_single_item_list(
    data: List[Dict[str, Any]] | Dict[str, Any],
) -> Dict[str, Any] | List[Dict[str, Any]]:
    """
    Normalise une liste contenant un seul élément en retournant cet élément.

    Args:
        data (Union[List[Dict[str, Any]], Dict[str, Any]]): Données à normaliser

    Returns:
        Union[Dict[str, Any], List[Dict[str, Any]]]: L'élément unique si data est une liste avec un seul élément, sinon data inchangé

    Raises:
        TypeError: Si data n'est pas une liste ou un dictionnaire
        ValueError: Si une liste vide est fournie
    """
    if not isinstance(data, (list, dict)):
        raise TypeError("Data must be a list or a dictionary")

    if isinstance(data, list):
        if len(data) == 1:
            return data[0]
        elif len(data) == 0:
            raise ValueError("Empty list provided")

    return data


def formate_text_response(
    data: List[Dict[str, Any]] | Dict[str, Any],
    root_keys: Sequence[str] = ROOT_KEYS,
    section_keys: Sequence[str] = SECTION_KEYS,
    article_keys: Sequence[str] = ARTICLE_KEYS,
) -> Dict[str, Any]:
    """
    Extrait les données de ConsultTextResponse model (LegiPart).

    Args:
        data (Union[List[Dict], Dict]): Liste de dictionnaires ou dictionnaire contenant le texte et les méta données recherchés
        root_keys (Sequence[str]): Liste des clés de la racine
        section_keys (Sequence[str]): Liste des clés pour la section
        article_keys (Sequence[str]): Liste des clés pour les articles

    Returns:
        Dict[str, Any]: Dictionnaire simplifiée, selon les clés retenues,
        du dictionnaire initial
    """
    # Normaliser les données d'entrée
    try:
        data = normalize_single_item_list(data)
    except ValueError:
        raise TypeError("Data must be a list with a single item")

    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary after normalization")

    # Extraction des métadonnées de la racine
    root_data = {key: data[key] for key in root_keys if key in data}

    # Traitement du contenu principal (sections à la racine)
    content = []
    if "sections" in data:
        content = [
            process_section(section, section_keys, article_keys)
            for section in data["sections"]
        ]

    # Assembler le résultat final
    return {"root": root_data, "content": content}


def formate_article_response(
    data: List[Dict[str, Any]] | Dict[str, Any],
    article_keys: Sequence[str] = ARTICLE_KEYS,
) -> List[Dict[str, Any]] | Dict[str, Any]:
    """
    Extrait les données de the GetArticleResponse model (GetArticle).

    Args:
        data (Union[List[Dict[str, Any]], Dict[str, Any]]): Dict ou liste de dict contenant les articles et les données associées
        article_keys (Sequence[str]): Liste des clés spécifiques à un article à extraire

    Returns:
        Union[List[Dict[str, Any]], Dict[str, Any]]: Dictionnaire ou liste de dictionnaires simplifiés,
        selon les clés retenues
    """
    # Traiter les listes avec plusieurs éléments
    if isinstance(data, list) and len(data) > 1:
        return [formate_article_single(item, article_keys) for item in data]

    # Normaliser les données pour un élément unique
    try:
        normalized_data = normalize_single_item_list(data)
    except ValueError:
        raise ValueError("Empty list provided")

    if not isinstance(normalized_data, dict):
        raise TypeError("Data must be a dictionary after normalization")

    # Traiter un élément unique
    return formate_article_single(normalized_data, article_keys)


def print_legal_hierarchy(legal_list: List[Dict[str, Any]]) -> None:
    """
    Affiche la hiérarchie légale d'une liste d'éléments juridiques.

    Args:
        legal_list (List[Dict[str, Any]]): Liste d'éléments juridiques à afficher
    """
    for item in legal_list:
        if "title_id" in item:
            print(f"Title ID: {item['title_id']}")
            print(f"  Title CID: {item['title_cid']}")
            print(f"  Title: {item['title']}\n")
        elif "section_id" in item:
            print(f"  Section ID: {item['section_id']}")
            print(f"    Title: {item['title']}\n")
        elif "extract_id" in item:
            print(f"    Extract ID: {item['extract_id']}")
            print(f"      Number: {item['num']}")
            print(f"      Legal Status: {item['legal_status']}")
            print(f"      Date Version: {item['date_version']}")
            print(f"      Title: {item['title']}")
            print(f"      Values: {item['values']}\n")


def print_article(data: List[Dict[str, Any]]) -> None:
    """
    Affiche les informations principales des articles.

    Args:
        data (List[Dict[str, Any]]): Liste d'articles à afficher
    """
    for item in data:
        extracted_data = {
            "fullSectionTitre": item["article"]["fullSectionsTitre"],
            "etat": item["article"]["etat"],
            "num": item["article"]["num"],
            "texte": item["article"]["texte"][:30],
        }
        print(extracted_data)
        print("----------------------------------")
