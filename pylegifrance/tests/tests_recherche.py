#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:33:38 2023
Fonctions de test pour la recherche
@author: raphael
"""
import os

from pylegifrance.pipeline.pipeline import (
    Pipeline, CallApiStep, ExtractSearchResult, 
    GetArticleId, GetTextId, Formatters
    )
from pylegifrance.pipeline.pipeline_factory import recherche_CODE, recherche_LODA
from pylegifrance.process.formatters import formate_article_response, formate_text_response



def test_recherche_CODE_valide(): 
    
    recherche_CODE(code_name="Code civil", search="7")

def test_recherche_LODA_1article(): 

    loda_search_article = recherche_LODA(text='78-17', search='7')

def test_recherche_LODA_1text(): 

    loda_search_text = recherche_LODA(text='78-17')
    
def test_recherche_LODA_1decret():
    loda_search_decret = recherche_LODA(text='2023-823', nature=["DECRET"])

def test_recherche_LODA_term(): 
    loda_search_empty_num_article = recherche_LODA(text='78-17',
                                                   search='poursuite',
                                                   champ='ALL')

def test_recherche_LODA_empty_text(): 
    loda_search_empty_text = recherche_LODA(search='autorité')
    
    
def test_recherche_LODA_wrong_field(): 
    loda_search_empty_num_article = recherche_LODA(text='78-17',
                                                   search='poursuite',
                                                   champ='RAISON SOCIALE')

def test_recherche_LODA_wrong_fond(): 
    loda_search_empty_num_article = recherche_LODA( text='78-17',
                                                   search='poursuite', 
                                                   champ='ALL',
                                                   fond="LOI")


def test_recherche_CODE_1article(): 

    code_search_article = recherche_CODE(code_name="Code civil",
                                         search='1200',
                                         formatter=True)   

def test_recherche_CODE_all(): 

    code_all = recherche_CODE(code_name="Code civil",
                              formatter=True)

def test_recherche_CODE_term(): 
    code_search_term = recherche_CODE(code_name="Code civil",
                                      search='mineur',
                                      champ="ARTICLE",
                                      formatter=True)   
    
def test_recherche_CODE_term_page2(): 
    code_search_term = recherche_CODE(code_name="Code civil",
                                      search='mineur',
                                      champ="ARTICLE",
                                      page_number=2, 
                                      formatter=True) 

def test_recherche_CODE_wrong_code(): 
    code_wrong_code = recherche_CODE(code_name="inexistant",
                                     search='mineur',
                                     champ="ARTICLE",
                                     formatter=True) 
    
    
def test_recherche_CODE_wrong_field(): 
    code_wrong_field = recherche_CODE(code_name="Code civil",
                                     search='7',
                                     champ="NUM",
                                     formatter=True)

def test_recherche_CODE_wrong_fond(): 
    code_wrong_fond = recherche_CODE(code_name="Code civil",
                                     search='7',
                                     champ="NUM_ARTICLE",
                                     fond="LODA_DATE",
                                     formatter=True)




