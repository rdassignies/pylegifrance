#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe permettant de gérer un pipeline générique de traitement des résultats
renvoyés par l'API Legifrance.

@author: Raphael d'Assignies'
"""

from pydantic import BaseModel
from typing import List, Union, Dict, Any
import logging
import json

from pylegifrance.models.consult import GetArticle, LegiPart
from pylegifrance.process.processors import (
    search_response_DTO,
    get_article_id,
    get_text_id,
)
from pylegifrance.process.formatters import (
    formate_text_response,
    formate_article_response,
)


logger = logging.getLogger(__name__)


class PipelineStep:
    """
    Classe de base pour une étape dans le pipeline de traitement.
    """

    def process(self, data, data_type=""):
        """
        Méthode de traitement des données à implémenter par chaque sous-classe.

        Args:
            data: Données à traiter.
            data_type: Type des données à traiter.

        Returns:
            Tuple[Any, str]: Données transformées et leur type.
        """
        raise NotImplementedError


class Pipeline:
    """
    Classe représentant un pipeline de traitement de données.

    Attributs:
        steps (List[PipelineStep]): Liste des étapes du pipeline.
    """

    def __init__(self, steps: List[PipelineStep]):
        self.steps = steps

    def execute(self, data: Any, data_type: str = "") -> Any:
        """
        Exécute chaque étape du pipeline, en faisant passer les données
        à travers chacune d'entre elles.

        Args:
            data (Any): Données à traiter par le pipeline.
            data_type (str): Type initial des données.

        Returns:
            Any: Données transformées après être passées à travers
                 toutes les étapes du pipeline.
        """
        for step in self.steps:
            # Si on a déjà une erreur, on arrête le pipeline et on retourne l'erreur
            if isinstance(data, dict) and "error" in data:
                logger.warning(f"Pipeline stopped due to error: {data['error']}")
                return data

            data, data_type = step.process(data, data_type)
            logger.debug(f"Type de données de l'étape : {data_type}")

            # Si une étape a retourné une erreur, on arrête le pipeline
            if data_type == "error":
                logger.warning("Pipeline stopped due to error in step")
                return data

        return data


class ExtractSearchResult(PipelineStep):
    """
    Une étape du pipeline pour l'extraction des résultats de recherche.
    """

    def process(self, data, data_type=""):
        """
        Extrait les résultats de recherche d'une réponse d'API.

        Args:
            data (requests.models.Response): La réponse de l'API contenant les résultats de recherche.
            data_type (str): Type des données d'entrée (non utilisé dans cette étape).

        Returns:
            Tuple[Any, str]: Résultats de recherche extraits et leur type.

        Raises:
            ValueError: Si la clé 'results' n'est pas trouvée dans la réponse.
        """
        extracted_data = search_response_DTO(data)
        return extracted_data, "ExtractSearchResult"


class GetArticleId(PipelineStep):
    """
    Une étape du pipeline pour récupérer les identifiants d'articles LEGIARTI.
    """

    def process(self, data, data_type=""):
        """
        Génère des modèles GetArticle à partir des données fournies.

        Args:
            data (List[dict]): Une liste de résultats avec des identifiants.
            data_type (str): Type des données d'entrée, doit être "ExtractSearchResult".

        Returns:
            Tuple[List[GetArticle], str]: Une liste d'objets GetArticle et le nom du type.

        Raises:
            TypeError: Si les données fournies ne sont pas dans le format correct
                      pour extraire les identifiants d'articles.
        """
        if data_type != "ExtractSearchResult":
            raise TypeError(
                "Les données pour extraire les identifiants d'articles"
                " ne sont pas dans le format correct"
            )

        article_ids = get_article_id(data)
        return article_ids, GetArticle.__name__


class GetTextId(PipelineStep):
    """
    Une étape du pipeline pour récupérer les identifiants de textes LEGITEXT.
    """

    def process(self, data, data_type="") -> tuple[Any, str]:
        """
        Génère des modèles LegiPart à partir des données fournies.

        Args:
            data (List[dict]): Une liste de résultats avec des identifiants.
            data_type (str): Type des données d'entrée, doit être "ExtractSearchResult".

        Returns:
            Tuple[List[LegiPart], str]: Une liste d'objets LegiPart et le nom du type.

        Raises:
            TypeError: Si les données fournies ne sont pas dans le format correct
                      pour extraire les identifiants de textes.
        """
        if data_type != "ExtractSearchResult":
            raise TypeError(
                "Les données pour extraire les identifiants de textes ne sont "
                "pas dans le format correct"
            )

        text_id = get_text_id(data)
        return text_id, LegiPart.__name__


class CallApiStep(PipelineStep):
    """
    Étape d'appel d'API dans le pipeline.

    Attributs:
        client (LegifranceClient): Client pour appeler l'API.
    """

    def __init__(self, client):
        self.client = client

    def process(self, data: Union[BaseModel, List[BaseModel], Dict], data_type=""):
        """
        Appelle l'API LegiFrance en utilisant les modèles (payload).

        Args:
            data (Union[BaseModel, List[BaseModel], Dict]): Modèles Pydantic
            pour générer le payload ou dictionnaire d'erreur.

        Raises:
            ValueError: Lève une erreur si le modèle n'est pas un type Pydantic.

        Returns:
            Soit un objet 'requests.models.Response' ou une liste
            d'objets 'requests.models.Response'.
        """

        # Si data est un dictionnaire avec une clé 'error', on le retourne directement
        if isinstance(data, dict) and "error" in data:
            logger.warning(f"Error detected in pipeline: {data['error']}")
            return data, "error"

        # Vérifie si 'data' est un modèle Pydantic ou une liste de modèles
        if isinstance(data, BaseModel):
            # Traitement pour un seul modèle Pydantic
            return self._call_api_single(data)
        elif isinstance(data, list) and all(
            isinstance(item, BaseModel) for item in data
        ):
            # Traitement pour une liste de modèles Pydantic
            return self._call_api_multiple(data)
        else:
            raise ValueError(
                "Les données d'entrée doivent être un modèle Pydantic "
                "ou une liste de modèles Pydantic"
            )

    def _call_api_single(self, model: BaseModel) -> tuple[Any, Any | None]:
        """
        Appelle l'API avec une seule requête (modèle).

        Args:
            model (BaseModel): Modèle Pydantic utilisé pour générer le payload.

        Returns:
            Tuple[Any, Any | None]: Contenu de la réponse JSON et le type de modèle de réponse.
        """
        route = getattr(model, "route", None)
        payload = model.model_dump(mode="json")

        response = self.client.call_api(route=route, data=payload)

        logger.debug(
            f"Appel API vers {route} retourné code de statut {response.status_code}"
        )

        model_reponse = getattr(model, "model_reponse", None)
        response_content = json.loads(response.content.decode("utf-8"))

        return response_content, model_reponse

    def _call_api_multiple(
        self, models: List[BaseModel]
    ) -> tuple[list[Any], Any | None]:
        """
        Appelle l'API avec une liste de requêtes (modèles).

        Args:
            models (List[BaseModel]): Liste de modèles Pydantic utilisés
                                      pour générer les payloads.

        Returns:
            Tuple[List[Any], Any | None]: Liste des contenus de réponses JSON
                                         et le type de modèle de réponse.
        """
        responses = []

        for model in models:
            route = getattr(model, "route", None)
            payload = model.model_dump(mode="json")

            response = self.client.call_api(route=route, data=payload)
            response_content = json.loads(response.content.decode("utf-8"))
            responses.append(response_content)

            logger.debug(
                f"Appel API vers {route} retourné code de statut {response.status_code}"
            )

        # Utilise le model_reponse du premier modèle pour tous les résultats
        model_reponse = getattr(models[0], "model_reponse", None)

        return responses, model_reponse


class Formatters(PipelineStep):
    """
    Étape de formattage des résultats de l'API.
    """

    def __init__(self, model: str = "default"):
        self.model = model

    def process(self, data: Dict[str, Any], data_type: str = "") -> tuple[Any, str]:
        """
        Formate un texte ou un article selon le type de données.

        Args:
           data (Dict[str, Any]): Données de réponse (GetArticleResponse ou ConsultTextResponse).
           data_type (str): Type des données d'entrée ("GetArticleResponse" ou "ConsultTextResponse").

        Returns:
           Tuple[Any, str]: Résultats reformattés et leur type.
        """
        if data_type == "GetArticleResponse":
            articles = formate_article_response(data)
            return articles, str(type(articles))

        if data_type == "ConsultTextResponse":
            text = formate_text_response(data)
            return text, str(type(text))

        # Si le type de données n'est pas reconnu, retourne None
        return None, "None"
