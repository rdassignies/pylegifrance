#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:57:20 2023

@author: Raphaël d'Assignies
"""

from typing import Union
import json
from models.consult import GetArticle, LegiPart
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def search_response_DTO(results:Union[dict, str]):
    """
    Cette fonction extrait les données du modèle de réponse SearchResponseDTO
    (RechercheFinal)

    Parameters
    ----------
    results : Dict
        Dictionnaire des résultats (clé 'results') renvoyé par l'API Legifrance

    Returns
    -------
    extracted_data : List
        Retourne une liste à plat des différents ids (text, section, article)

    """
    if isinstance(results, str):
       try:
           # Essayer de parser data en tant que JSON
           results = json.loads(results)
       except json.JSONDecodeError:
           raise ValueError("La chaîne 'results' n'est pas un JSON valide.")

    elif not isinstance(results, dict):
       raise TypeError("Le paramètre 'results' doit être un dictionnaire ou une chaîne JSON.")

    
    extracted_data = []
    
    # Fonction récursive pour parcourir les éléments
    def extract_recursive(element):
        # Extraire les données de 'titles' si elles existent
        if 'titles' in element:
            for title in element['titles']:
                extracted_data.append({
                    'title_id': title.get('id', ''),
                    'title_cid': title.get('cid', ''),
                    'title': title.get('title', '')
                })

        # Extraire les données de 'sections' si elles existent
        if 'sections' in element:
            for section in element['sections']:
                extracted_data.append({
                    'section_id': section.get('id', ''),
                    'title': section.get('title', ''),
                })
                # Appel récursif pour les extracts dans les sections
                if 'extracts' in section:
                    for extract in section['extracts']:
                        extracted_data.append({
                            'extract_id': extract.get('id', ''),
                            'num': extract.get('num', ''),
                            'legal_status': extract.get('legalStatus', ''),
                            'date_version': extract.get('dateVersion', ''),
                            'title': extract.get('title', ''),
                            'values': extract.get('values', '')
                        })

    # Appel initial sur les résultats
    for result in results['results']:
        extract_recursive(result)

    return extracted_data

def get_text_id(data) : 
    """
    

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.

    Raises
    ------
    GetTextIdError
        DESCRIPTION.

    Returns
    -------
    None.

    """
    # Log des informations de traitement
    logger.debug("GetArticleInstances : RECUPERATION DES LEGIARTI -------------")
    
    text_ids = []
    for item in data:

        if 'title_id' in item and item['title_id'].startswith('LEGITEXT'):
            text_ids.append(LegiPart(textId=item['title_id']))
    
    logger.debug(f"Taille des données contenant les LEGITEXT :{len(text_ids)}")
    
    if not text_ids:
        raise GetTextIdError("La liste GetText est vide" 
                             "- Aucun LEGITEXT trouvé dans les données."
                             "Vérifier les critères de recherche.")
    return text_ids

def get_article_id(data): 
       # Log des informations de traitement
    logger.debug("GetArticleInstances : RECUPERATION DES LEGIARTI -------------")
    
    article_ids = []
    for item in data:
        if 'extract_id' in item and item['extract_id'].startswith('LEGIARTI'):
            article_ids.append(GetArticle(id=item['extract_id']))
       
    logger.debug(f"Taille des données contenant les LEGIARTI : {len(article_ids)}")
    
    if not article_ids:
        raise GetArticleIdError("La liste GetArticle est vide" 
                                       "- Aucun LEGIARTI trouvé dans les données."
                                       "Vérifier les critères de recherche.")
    
    return article_ids


class GetArticleIdError(Exception):
    """Exception levée lorsque la liste GetArticle est vide."""
    pass

class GetTextIdError(Exception):
    """Exception levée lorsque la liste GetLegiPart est vide."""
    pass

    
