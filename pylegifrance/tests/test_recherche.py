#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:33:38 2023

@author: raphael
"""
from pipeline.pipeline_factory import recherche_CODE
from pipeline.pipeline import (
    Pipeline, CallApiStep, ExtractSearchResult, 
    GetArticleId, GetTextId, Formatters
    )
def test_recherche_CODE_valide(client): 
    
    r = recherche_CODE(client, nom_code="Code civil", search="7")
    
    return r 

