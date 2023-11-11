#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:57:20 2023

@author: raphael
"""
from models.models import * 


texte = []
def process_articles(articles) : 
   
    
    texte.append(articles)
    for art in articles : 
        #print(art['cid'], ' / ', art['etat'])
        print("-----------------------")


def process_sections(sections, depth=3):
    
    for section in sections:
        if section['etat'] == 'VIGUEUR':
            if 'articles' in section:
                print(section['title'])
                process_articles(section['articles'])
            if 'sections' in section and len(section['sections']) > 0:
                process_sections(section['sections'], depth + 1)
                
   
def display(sections) : 
    for items in sections : 
        print(items['title'])
        
        for item in items['articles'] : 
            print(item['cid'])
            #for art in item : 
            #    print(art)
            #print(items['title'])
            #print("______________________ ______________")
            #print(f"Articles : {item['articles']}")
            #print(f"{item['title']}")

def extract_data(results):
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
                            'title': extract.get('title', ''), 
                            'values' : extract.get('values', '') 
                        })

    # Appel initial sur les résultats
    for result in results:
        extract_recursive(result)

    return extracted_data

def create_get_article_instances(data):
    get_article_instances = []
    for item in data:
        if 'extract_id' in item and item['extract_id'].startswith('LEGIARTI'):
            get_article_instances.append(GetArticle(id=item['extract_id']))
    return get_article_instances.model_dump(mode='json')
