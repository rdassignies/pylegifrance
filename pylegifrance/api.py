#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests 
import time
import json
from uuid import uuid4
from inspect import Signature, Parameter

from requests_oauthlib import OAuth2Session


_API_HOST = ''
_TOKEN_URL = 'https://oauth.piste.gouv.fr/api/oauth/token'

#TODO : ajouterload env pour les var d'environnements

"""
load_dotenv()
client_id = os.getenv("OAUTH_CLIENT_ID")
client_secret = os.getenv("OAUTH_CLIENT_SECRET")
"""

class LegiHandler:

    def __init__(
                 self,
                 legifrance_api_key="e3167bf1-93d2-4e6e-bc7b-cf759770de6b",
                 legifrance_api_secret="2bd78d98-d7fa-4835-9f61-fad6a7c41cd5"
                 ):

        self.token = ''
        self.client_id = legifrance_api_key
        self.client_secret = legifrance_api_secret
        self.token_url= 'https://oauth.piste.gouv.fr/api/oauth/token'
        self.api_url = 'https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/'
        self.time_token = time.time()
        self._get_access()
        
    
    def _get_access(self, attempts=3, delay=5):
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'openid'
        }
        
        for i in range(attempts):
            response = requests.post(self.token_url, data=data)
            if 200 <= response.status_code < 300:
                token = response.json().get('access_token')
                self.token = token
                self.expires_in = response.json().get('expires_in')
                self.client = OAuth2Session(self.client_id, token=token)
            else:
                if i < attempts - 1:  # Si ce n'est pas la dernière tentative
                    time.sleep(delay)  # Attendre avant la prochaine tentative
                else:
                    raise Exception(f"Erreur lors de l'obtention du token après {attempts} tentatives. Dernière erreur : {response.status_code} - {response.text}")
        
    def _update_client(self) : 
        
        elapsed_time = time.time() - self.time_token
        print("elapsed time : ", elapsed_time)
        if elapsed_time >= self.expires_in : 
            print("renouvellement du token")
            self.time_token = time.time()
            self._get_access()
            
        
    
    def call_api(self, route=None, data=None): #TODO ajouter le type pour data
            self._update_client()
            headers = {
                'Authorization': f'Bearer {self.token}',
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            if data is not None:
                #for d, i in data.items():
                #    print('route: ', route , '\n' , d , i , type(data)) #uniquement pour debug
            
                response = requests.post(f"{self.api_url}{route}",headers=headers, json=data)

            if response.status_code >= 400 and response.status_code < 500:
                raise Exception(f"Erreur client {response.status_code} - {response.text} lors de l'appel à l'API :")
      
            return response
        

    
    
    def ping(self, route:str = "list/ping") : 
        
        pass
    
    def get(self, route):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        print(f"{self.api_url}{route}")
        response = requests.get(f"{self.api_url}{route}", headers=headers)
        response.raise_for_status()
        self.data = response.json()
        
        return response


    