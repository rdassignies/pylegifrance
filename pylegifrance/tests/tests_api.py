#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 11:28:05 2023

@author: raphael
"""
import os, logging
from pylegifrance.client.api import LegiHandler
from dotenv import load_dotenv
import requests

from pylegifrance.models.consult import GetArticle



def test_initialisation_client_avec_vars_env() : 
    if load_dotenv():
        print("VAR CLIENT_ID: ", os.getenv("LEGIFRANCE_CLIENT_ID"))
        client = LegiHandler()
        client.set_api_keys()
        print("clés présentes: ", client.client_id, 'id mémoire :', id(client))
        
        #supression des clés 
        os.environ.pop("LEGIFRANCE_CLIENT_ID", None)
        os.environ.pop("LEGIFRANCE_CLIENT_SECRET", None)
        
        print("Après suppressin clés présentes: ", client.client_id, 'id mémoire :', id(client))
        
       

def test_initialisation_client_sans_vars_env() : 
   
        client = LegiHandler()
        print("clés présentes: ", client.client_id, 'id mémoire :', id(client))

        client.set_api_keys()
        
        if load_dotenv():
            print("VAR CLIENT_ID: ", os.getenv("LEGIFRANCE_CLIENT_ID"))
            print("Id mémoire: ", id(client))
            client.set_api_keys()
            print("Après création des vars d'env. ': ", client.client_id, 'id mémoire :', id(client))

def test_requete_simple(): 
    
     if load_dotenv():
         client = LegiHandler()
         client.set_api_keys()
         art = GetArticle(id="LEGIARTI000047362226")
         client.call_api(route=art.Config.route, data=art.model_dump(mode="json"))


def test_request_decompose(): 
    if load_dotenv():
        client = LegiHandler()
        client.client_id = os.getenv("LEGIFRANCE_CLIENT_ID")
        client.client_secret = os.getenv("LEGIFRANCE_CLIENT_SECRET")
        
        # get token
        data = {
            'grant_type': 'client_credentials',
            'client_id': client.client_id,
            'client_secret': client.client_secret,
            'scope': 'openid'
        }
        response_tok = requests.post(client.token_url, data=data)
        client.token = response_tok.json().get('access_token')
        
        art = GetArticle(id="LEGIARTI000047362226")
        root_logger = logging.getLogger()
        headers = {
            'Authorization': f'Bearer {client.token}',
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        print("Root logger avant appel requests: ", root_logger.getEffectiveLevel())
        url = client.api_url + art.Config.route
        response = requests.post(url ,headers=headers, json=art.model_dump(mode='json'))
        
        