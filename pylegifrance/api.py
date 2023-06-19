#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 09:13:33 2023

@author: raphael
"""

import requests 
import time
import json
from uuid import uuid4
from requests_oauthlib import OAuth2Session
from pylegifrance.models import routes

_API_HOST = 'https://api.aife.economie.gouv.fr/dila/legifrance-beta/lf-engine-app'
_TOKEN_URL = 'https://oauth.piste.gouv.fr/api/oauth/token'

class LegifranceClient:
    
    def __init__(self):
        self.token = ''
        self.client_id = "e3167bf1-93d2-4e6e-bc7b-cf759770de6b"
        self.client_secret = "2bd78d98-d7fa-4835-9f61-fad6a7c41cd5" #mettre en env 0bc3dd0c-3c1c-431d-aab0-0ef2b0a9fb2c
        self.token_url = 'https://oauth.piste.gouv.fr/api/oauth/token'
        self.api_url = 'https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/'
        self.docs = [] #stock les dictionnaires de metadonnées
        self.time_token = time.time()
        self.token = self._get_access_token()
        
        #with open(config_file, 'r') as f:
        #    self.config = json.load(f)
        
    def _get_access_token(self):
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'openid'
        }
        response = requests.post(self.token_url, data=data)
        self.token = response.json().get('access_token')
        #response.raise_for_status()
        #
    
    
    def _update_client(self) : 
        elapsed_time = time.time() - self.time_token
        if elapsed_time >= 3600 : 
            self.time_token = time.time()
            self.token = self._get_access_token()
    
    def ping(self, route:str = "list/ping") : 
        pass

    def get(self, route):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(self.api_url+route, headers=headers)
        response.raise_for_status()
        self.data = response.json()
        
        return response

    def post(
            self, 
            payload:dict, 
            route:str="search",
            full_name:str='', 
            save:bool=False
            ):
        
        """ Les principales routes : 
                "search" : recherche des données
                "consult/legiPart" : rapatrie toute la législation avec identfiant
                "consult/getArticle" : récupère un article
        """
        headers = {
            'Authorization': f'Bearer {self.token}',
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(f'{self.api_url}{route}', headers=headers, data=json.dumps(payload))
        
        #self.data = response.json()
    
        return response
    