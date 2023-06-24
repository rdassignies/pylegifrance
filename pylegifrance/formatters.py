#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:57:20 2023

@author: raphael
"""
#texte = []
def process_articles(articles) : 
    
    texte.append(articles)
    print(articles)
    print("-----------------------")


def process_sections(sections, depth=1):
    
    for section in sections:
        if section['etat'] == 'VIGUEUR':
            if 'articles' in section:
                process_articles(section['articles'])
            if 'sections' in section and len(section['sections']) > 0:
                process_sections(section['sections'], depth + 1)
                

def display(sections) : 
    for items in sections : 
        for item in items : 
            print(f"PathTitle : {item['pathTitle'][0]}")
            print(f"{item['num']}")
