#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module pour la création d'un pipeline de traitement de données.

@author: Raphael d'Assignies'
"""
from pydantic import BaseModel
from typing import List, Union
import logging
import json

from api import LegiHandler
from models.consult import GetArticle, LegiPart
from process.processors import (search_response_DTO, 
                                get_article_id, get_text_id)

from process.formatters import formate_text_response, formate_article_response


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Pipeline:
    """
    Classe représentant un pipeline de traitement de données.
    Attributs:
        steps (List[PipelineStep]): Liste des étapes du pipeline.
    """
    def __init__(self, steps):
        self.steps = steps

    def execute(self, data, data_type=""):
        """
        Exécute chaque étape du pipeline en passant les données à
        travers chacune d'elles.

        Paramètres:
            data: Données à traiter par le pipeline.

        Retourne:
            Données transformées après le passage dans toutes
            les étapes du pipeline.
        """
        for step in self.steps:
            data, data_type = step.process(data, data_type)
            logger.debug(f"Datatype de l'étape : {data_type}")

        return data

class PipelineStep:
    """
    Classe de base pour une étape dans le pipeline de traitement.
   
    """
 
        
    def process(self, data, data_type=""):
        """
        Méthode de traitement des données à implémenter par chaque sous-classe.

        Parameters:
            data: Données à traiter.

        Return:
            Données transformées.
        """
        raise NotImplementedError

class ExtractSearchResult(PipelineStep) : 
    """
    Étape d'extraction des résultats de recherche dans le pipeline.
    """
   #TODO : implémenter l'utilisation de data_type à partir du modèle de répons
    
    def process(self, data, data_type="") : 
        """
        Extrait les résultats de recherche à partir d'une réponse de l'API.

        Parameters:
            data (requests.models.Response): Réponse de l'API contenant les résultats de recherche.

        Return:
            Résultats de recherche extraits.

        Exceptions:
            ValueError: Si la clé 'results' n'est pas trouvée dans la réponse.
        """
        #TODO : vérifier que data soit une instance de requests.models.Response
        #TODO : gérer l'erreur si la clé results non présente
        data = search_response_DTO(data)
        return data, "ExtractSearchResult"
    
class GetArticleId(PipelineStep):
    """
    Étape de récupération des identifiants LEGIARTI dans le pipeline.
    """
    
    def process(self, data, data_type=""):
        """
        Génère des modèles GetArticle à partir des données fournies.

        Parameters:
            data (List[dict]): Liste de résultats avec les ids.

        Return:
            Liste de GetArticle (cf. models.models)
        """

        if data_type=="ExtractSearchResult":
            article_ids = get_article_id(data)
        else:
             raise TypeError("Les données pour extraire les articles id ne sont pas au bon format")

        return article_ids, GetArticle.__name__


class GetTextId(PipelineStep):
    """
    Étape de récupération des identifiants LEGITEXT dans le pipeline.
    """
    
    def process(self, data, data_type=""):
        """
        Génère des modèles LegiPart à partir des données fournies.

        Parameters:
            data (List[dict]): Liste de résultats avec les ids.

        Return:
            Liste de LegiPart (cf. models.models)
        """
       
        if data_type=="ExtractSearchResult":
            text_id = get_text_id(data)
        else: 
             raise TypeError("Les données pour extraire les articles id ne sont pas au bon format")

        return text_id, LegiPart.__name__

class CallApiStep(PipelineStep):
    """
    Étape d'appel d'API dans le pipeline.

    Attributs:
        client (LegiHandler): Client pour appeler l'API.
    """
    def __init__(self, client):
        self.client = client

    def process(self, data: Union[BaseModel, List[BaseModel]], data_type=""):
        """
        Appel l'API LegiFrance à partir des modèles (payload). 

        Parameters
        ----------
        data : Union[BaseModel, List[BaseModel]]
            Modèles pydantic permettant de générer le payload

        Raises
        ------
        ValueError
            Génère une erreur si le modèle n'est pas de type pydantic

        Returns
        -------
        requests.models.Response
            Renvoi un objet Response du module requests
        ou
        List[requests.models.Response]
            Renvoi une liste d'objets Response du module requests

        """

        # Vérifie si 'data' est un modèle Pydantic ou une liste de modèles
        if isinstance(data, BaseModel):
            # Traitement pour un seul modèle Pydantic
            return self._call_api_single(data)
        elif isinstance(data, list) and all(isinstance(item, BaseModel) for item in data):
            # Traitement pour une liste de modèles Pydantic
            return self._call_api_multiple(data)
        else:
            raise ValueError("Input data must be a Pydantic model or a list of Pydantic models")

    def _call_api_single(self, model: BaseModel):
        """
        Appel de l'API avec une seule requête (un modèle)

        Parameters
        ----------
        model : BaseModel
            Modèles pydantic permettant de générer le payload

        Returns
        -------
        response : requests.models.Response
            Renvoi une liste d'objets Response du module requests

        """
        # Logique pour appeler l'API avec un seul modèle
        response = self.client.call_api(
            route=model.Config.route,
            data=model.model_dump(mode='json')
        )

        # Log des informations de la réponse
        logger.debug(f"---------- call_api_SINGLE -------------")
        logger.debug(f"API call to {model.Config.route} returned status code {response.status_code}")
        # logger.debug(f"Response Headers: {response.headers}")
        logger.debug(f"Response Body: {response.text}")

        return json.loads(response.content.decode('utf-8')), model.Config.model_reponse

    def _call_api_multiple(self, models: List[BaseModel]):
        
        """
        Appel de l'API avec une liste de requêtes (modèles)

        Parameters
        ----------
        models : List[BaseModel]
            Liste de modèles pydantic permettant de générer le payload

        Returns
        -------
        responses : List[requests.models.Response]
            Renvoi une liste d'objets Response du module requests

        """
        # Logique pour appeler l'API avec plusieurs modèles
        responses = []
        for model in models:
            response = self.client.call_api(
                route=model.Config.route,
                data=model.model_dump(mode='json')
            )
            responses.append(json.loads(response.content.decode('utf-8')))

            # Log des informations de la réponse
            logger.debug(f"---------- call_api_MULTIPLE -------------")
            logger.debug(f"API call to {model.Config.route} returned status code {response.status_code}")
            #logger.debug(f"Response Headers: {response.headers}")
            #logger.debug(f"Response Body: {response.text}")

        return responses, models[0].Config.model_reponse

class Formatters(PipelineStep) : 
      """
      Etape de formatage des résultats 
      """
      def process(self, data, data_type=""): 
          """
          Fonction qui formatte les réponses (article ou texte)

          Parameters
          ----------
          data : Dict
              GetArticleResponse ou ConsultTextResponse
          data_type : String, optional
              GetArticleResponse ou ConsultTextResponse
          Returns
          -------
          Type : Dict
              Dictionnaire de données reformatées
              

          """
          if data_type=="GetArticleResponse":
              articles = formate_article_response(data[0])

              return articles, str(type(articles))

          if data_type=="ConsultTextResponse":
              text = formate_text_response(data[0], )
              
              return text, str(type(text))
          
       
              
              

