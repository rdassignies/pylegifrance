#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:57:20 2023

@author: Raphaël d'Assignies

"""
# TODO : à mettre dans une fichier de configuration (YAML)
ARTICLE_KEYS = ('pathTitle', 'content', 'num', 'fullSectionsTitre', 
                'texte','etat','VersionArticle' )
ROOT_KEYS = ('cid', 'title')
SECTION_KEYS = ('title', 'cid')


def formate_text_response(data,
                          root_keys=ROOT_KEYS, 
                          section_keys=SECTION_KEYS, 
                          article_keys=ARTICLE_KEYS):
    """
    Cette fonction extrait les données du modèle de réponse ConsultTextResponse
    (LegiPart)

    Parameters
    ----------
    data : List
        DESCRIPTION.
    root_keys : Tuple
       liste des clés à la racine de la structure
    article_keys : Tuple
        liste des clés spécifiques à un article
    section_keys : Tuple
       liste des clés spécifiques à section

    Returns
    -------
    TYPE : Dict
       Dictionnaire représentant une structure simplifiée de la structure originale

    """
    # Fonction interne pour traiter récursivement les sections et articles
    def process_section(section_data):
        section_result = {}

        # Extraire les données des articles dans la section
        if 'articles' in section_data:
            section_result['articles'] = [
                {key: article[key] for key in article_keys if key in article}
                for article in section_data['articles']
            ]

        # Extraire les données de la section elle-même
        section_result['section_data'] = {key: section_data[key] for key in section_keys if key in section_data}

        # Traiter les sous-sections récursivement
        if 'sections' in section_data:
            section_result['subsections'] = [
                process_section(subsection) for subsection in section_data['sections']
            ]

        return section_result

    # Extraction des métadonnées de la racine
    root_data = {key: data[key] for key in root_keys if key in data}

    # Traitement du contenu principal (sections à la racine)
    content = []
    if 'sections' in data:
        content = [process_section(section) for section in data['sections']]

    # Assembler le résultat final
    return {"root": root_data, "content": content}

def formate_article_response(data, article_keys=ARTICLE_KEYS): 
    """
    Cette fonction extrait les données du modèle de réponse GetArticleResponse
    (GetArticle)

    Parameters
    ----------
    data : Dict
        Dictionnaire comprenant l'intégralité de la réponse
    article_keys : Tuple
        liste des clés spécifiques à un article

    Returns
    -------
    simplified_dict : Dict
        Dictionnaire représentant une structure simplifiée de la structure originale

    """
    # TODO: Vérifier si la valeur de la clé est none et l'exclure
    simplified_dict = {}
    # Accès à la sous-structure 'article'
    article = data.get("article", {})
    for key in article_keys:
        try:
            # Extraction de la valeur pour chaque clé
            value = article[key]
            simplified_dict[key] = value
        except KeyError:
            # Gestion du cas où la clé n'est pas trouvée
            simplified_dict[key] = None  # ou 'raise KeyError' pour signaler l'absence de la clé
    return simplified_dict



def print_legal_hierarchy(legal_list):
    for item in legal_list:
        if 'title_id' in item:
            print(f"Title ID: {item['title_id']}")
            print(f"  Title CID: {item['title_cid']}")
            print(f"  Title: {item['title']}\n")
        elif 'section_id' in item:
            print(f"  Section ID: {item['section_id']}")
            print(f"    Title: {item['title']}\n")
        elif 'extract_id' in item:
            print(f"    Extract ID: {item['extract_id']}")
            print(f"      Number: {item['num']}")
            print(f"      Legal Status: {item['legal_status']}")
            print(f"      Date Version: {item['date_version']}")
            print(f"      Title: {item['title']}")
            print(f"      Values: {item['values']}\n")
            

def print_article(data) : 
    for item in data : 
        extracted_data = {
        'fullSectionTitre': item['article']['fullSectionsTitre'],
        'etat': item['article']['etat'],
        'num':  item['article']['num'],
        'texte': item['article']['texte'][:30]
        }
        print(extracted_data)
        print("----------------------------------")