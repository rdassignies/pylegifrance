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
import inspect
from inspect import Parameter

from requests_oauthlib import OAuth2Session

_API_HOST = 'https://api.aife.economie.gouv.fr/dila/legifrance-beta/lf-engine-app'
_TOKEN_URL = 'https://oauth.piste.gouv.fr/api/oauth/token'

"""
load_dotenv()
client_id = os.getenv("OAUTH_CLIENT_ID")
client_secret = os.getenv("OAUTH_CLIENT_SECRET")
"""

class LegiHandler:
    
    def __init__(self):
        self.token = ''
        self.client_id = "e3167bf1-93d2-4e6e-bc7b-cf759770de6b"
        self.client_secret = "2bd78d98-d7fa-4835-9f61-fad6a7c41cd5" #mettre en env 0bc3dd0c-3c1c-431d-aab0-0ef2b0a9fb2c
        self.token_url = 'https://oauth.piste.gouv.fr/api/oauth/token'
        self.api_url = 'https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/'
        self.docs = [] #stock les dictionnaires de metadonnées
        self.time_token = time.time()
        self._get_access_token()
        
        self.post_headers = {
            'Authorization': f'Bearer {self.token}',
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        from models import routes
        self.routes = routes
        
        for route in routes.keys():
            method_name = route.replace('/', '_').strip('_')  # Convertir la route en nom de méthode
            method = self._create_method(route)
            setattr(self, method_name, method)
        
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
        if 200 <= response.status_code < 300:
                self.token = response.json().get('access_token')
        else : 
            raise Exception(f"Erreur lors de l'obtention du token erreur : {response.status_code}")
        
    
    
    def _update_client(self) : 
        elapsed_time = time.time() - self.time_token
        if elapsed_time >= 3600 : 
            self.time_token = time.time()
            self.token = self._get_access_token()
            
            
    def _create_method(self, route):
        # Créer une nouvelle méthode qui appelle l'API avec les données fournies
        def method(**data):
            # Utiliser les valeurs par défaut de la route si une clé n'est pas présente dans les données
            default_data = {key: data.get(key, value) for key, value in self.routes[route].items()}
            # Si data est vide, utiliser default_data
            if not data:
                data = default_data
            return self.call_api(route, data)
        
        # Créer une nouvelle signature pour la méthode avec les paramètres de la route
        params = [Parameter(key, Parameter.KEYWORD_ONLY, default=value) for key, value in self.routes[route].items()]
        method.__signature__ = inspect.Signature(params)

        # Ajouter une docstring à la méthode
        method.__doc__ = f"Appelle l'API avec la route '{route}' et les données suivantes : {self.routes[route]}"

        return method


    def _validate_data(self, route, data):
        # Vérifiez que toutes les clés nécessaires sont présentes
        for key in self.routes[route].keys():
            if key not in data:
                raise ValueError(f"La clé '{key}' est manquante dans" 
                                 "les données fournies pour la route {route}")
            if not data[key]:
                raise ValueError(f"La clé '{key}' n'a pas de valeur associée"
                                 "dans les données fournies pour la route {route}")
   
        
    
    def call_api(self, route, data):
       
        self._validate_data(route, data)
        response = requests.post(f"{self.api_url}{route}",headers=self.post_headers, json=data)
        
        if response.status_code >= 400 and response.status_code < 500:
            raise Exception(f"Erreur client  {response.status_code} lors de l'appel à l'API :")
  
        return response
    

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

    def _post(
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
    