#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 11:28:05 2023

@author: raphael
"""
import os
from client.api import LegiHandler
from dotenv import load_dotenv


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
