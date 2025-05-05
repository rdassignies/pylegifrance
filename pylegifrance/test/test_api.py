#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 11:28:05 2023

@author: raphael
"""

import os
import logging
from pylegifrance.client.api import LegiHandler
from dotenv import load_dotenv
import requests

from pylegifrance.models.consult import GetArticle


def test_initialisation_client_avec_vars_env():
    if load_dotenv():
        print("VAR CLIENT_ID: ", os.getenv("LEGIFRANCE_CLIENT_ID"))
        client = LegiHandler()
        client.set_api_keys()
        print("clés présentes: ", client.client_id, "id mémoire :", id(client))

        # supression des clés
        os.environ.pop("LEGIFRANCE_CLIENT_ID", None)
        os.environ.pop("LEGIFRANCE_CLIENT_SECRET", None)

        print(
            "Après suppressin clés présentes: ",
            client.client_id,
            "id mémoire :",
            id(client),
        )


def test_initialisation_client_sans_vars_env():
    client = LegiHandler()
    print("clés présentes: ", client.client_id, "id mémoire :", id(client))

    client.set_api_keys()

    if load_dotenv():
        print("VAR CLIENT_ID: ", os.getenv("LEGIFRANCE_CLIENT_ID"))
        print("Id mémoire: ", id(client))
        client.set_api_keys()
        print(
            "Après création des vars d'env. ': ",
            client.client_id,
            "id mémoire :",
            id(client),
        )


def test_requete_simple():
    if load_dotenv():
        client = LegiHandler()
        client.set_api_keys()
        art = GetArticle(id="LEGIARTI000047362226")
        client.call_api(
            route=art.model_config["route"], data=art.model_dump(mode="json")
        )


def test_request_decompose():
    if load_dotenv():
        client = LegiHandler()
        client.client_id = os.getenv("LEGIFRANCE_CLIENT_ID")
        client.client_secret = os.getenv("LEGIFRANCE_CLIENT_SECRET")

        # get token
        data = {
            "grant_type": "client_credentials",
            "client_id": client.client_id,
            "client_secret": client.client_secret,
            "scope": "openid",
        }
        response_tok = requests.post(client.token_url, data=data)
        client.token = response_tok.json().get("access_token")

        art = GetArticle(id="LEGIARTI000047362226")
        root_logger = (
            logging.getLogger()
        )  # Variable utilisée uniquement pour debug du logger (niveau)
        headers = {
            "Authorization": f"Bearer {client.token}",
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        print(
            "Root logger level before requests call: ", root_logger.getEffectiveLevel()
        )
        url = client.api_url + art.model_config["route"]
        requests.post(url, headers=headers, json=art.model_dump(mode="json"))


def test_ping_success_real():
    """
    Teste la méthode ping avec l'API réelle pour une réponse réussie.
    Nécessite que des identifiants API valides soient définis dans les variables d'environnement.
    """
    client = LegiHandler()

    # Définir les clés API à partir des variables d'environnement
    client.set_api_keys(
        os.getenv("LEGIFRANCE_CLIENT_ID"),
        os.getenv("LEGIFRANCE_CLIENT_SECRET"),
    )

    try:
        # Effectuer le ping
        success = client.ping()
        assert success is True, "Ping should return True for a valid API connection."
        print("Ping Success Test Passed: Connection to API is valid.")
    except Exception as e:
        print(f"Test Ping Failed with Exception: {e}")
        assert False, f"Ping failed while testing: {e}"
