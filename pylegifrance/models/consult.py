from typing import Optional
from datetime import datetime


from pydantic import BaseModel

# Consult Controler
# TODO: A compléter avec tous les chemins de /consult


class Jorf(BaseModel):
    """
    Récupère le contenu d'un texte du fonds JORF à partir de son identifiant

    """
    textCid: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/jorf"
        model_reponse = "ConsultTextResponse"


class LegiPart(BaseModel):
    """
    Récupère le contenu d'un texte du fonds LEGI
    à partir de son identifiant et de sa date de vigueur

    """

    date: str = datetime.now().strftime("%Y-%m-%d")
    textId: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/legiPart"
        model_reponse = "ConsultTextResponse"


class GetSectionByCid(BaseModel):
    """
    Récupère la liste des section par leur identifiant commun

    """

    cid: str

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/getSectionByCid"


class GetArticle(BaseModel):
    """
    Récupère un article par son identifiant

    """
    id: str

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """

        route = "consult/getArticle"
        model_reponse = 'GetArticleResponse'
