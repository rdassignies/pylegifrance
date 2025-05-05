from typing import Optional, List
from datetime import datetime


from pydantic import BaseModel, Field

# Consult Controler
# Models for the /consult endpoints


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


class GetArticleWithIdEliOrAlias(BaseModel):
    """
    Récupère un article par son identifiant ELI ou son alias
    """
    id: str

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/getArticleWithIdEliOrAlias"
        model_reponse = "GetArticleResponse"


class GetArticleByCid(BaseModel):
    """
    Récupère un article par son identifiant CID
    """
    cid: str

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/getArticleByCid"
        model_reponse = "GetListArticleResponse"


class CodeConsult(BaseModel):
    """
    Récupère le contenu d'un code à partir de son identifiant et de sa date de vigueur
    """
    date: str = datetime.now().strftime("%Y-%m-%d")
    textId: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/code"
        model_reponse = "ConsultTextResponse"


class CodeConsultWithAncienId(BaseModel):
    """
    Récupère le contenu d'un code à partir de son ancien identifiant
    """
    ancienId: str
    date: str = datetime.now().strftime("%Y-%m-%d")
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/getCodeWithAncienId"
        model_reponse = "ConsultTextResponse"


class CnilConsult(BaseModel):
    """
    Récupère le contenu d'un texte CNIL à partir de son identifiant
    """
    textCid: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/cnil"
        model_reponse = "ConsultCnilTextResponse"


class CnilConsultWithAncienId(BaseModel):
    """
    Récupère le contenu d'un texte CNIL à partir de son ancien identifiant
    """
    ancienId: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/getCnilWithAncienId"
        model_reponse = "ConsultCnilTextResponse"


class JuriConsult(BaseModel):
    """
    Récupère le contenu d'un texte jurisprudentiel à partir de son identifiant
    """
    textId: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/juri"
        model_reponse = "ConsultJuriTextResponse"


class JuriConsultWithAncienId(BaseModel):
    """
    Récupère le contenu d'un texte jurisprudentiel à partir de son ancien identifiant
    """
    ancienId: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/getJuriWithAncienId"
        model_reponse = "ConsultJuriTextResponse"


class JorfConsult(BaseModel):
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
        model_reponse = "ConsultJorfResponse"


class JorfConsultWithNor(BaseModel):
    """
    Récupère le contenu d'un texte du fonds JORF à partir de son numéro NOR
    """
    nor: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/getJoWithNor"
        model_reponse = "ConsultJorfResponse"


class JorfContConsult(BaseModel):
    """
    Récupère le contenu d'un JO à partir de son identifiant
    """
    contId: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/jorfCont"
        model_reponse = "GetJosResponse"


class LastNJo(BaseModel):
    """
    Récupère les N derniers JO
    """
    n: int = Field(..., description="Nombre de JO à récupérer")

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/lastNJo"
        model_reponse = "GetJorfContResponse"


class KaliTextConsult(BaseModel):
    """
    Récupère le contenu d'un texte KALI à partir de son identifiant
    """
    textId: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/kaliText"
        model_reponse = "ConsultKaliTextResponse"


class KaliTextConsultArticle(BaseModel):
    """
    Récupère un article d'un texte KALI à partir de son identifiant
    """
    textId: str
    articleId: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/kaliArticle"
        model_reponse = "ConsultKaliTextResponse"


class KaliTextConsultSection(BaseModel):
    """
    Récupère une section d'un texte KALI à partir de son identifiant
    """
    textId: str
    sectionId: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/kaliSection"
        model_reponse = "ConsultKaliTextResponse"


class KaliContConsult(BaseModel):
    """
    Récupère le contenu d'un conteneur KALI à partir de son identifiant
    """
    contId: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/kaliCont"
        model_reponse = "ConsultKaliContResponse"


class KaliContConsultIdcc(BaseModel):
    """
    Récupère le contenu d'un conteneur KALI à partir de son IDCC
    """
    idcc: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/kaliContIdcc"
        model_reponse = "ConsultKaliContResponse"


class LegiSommaireConsult(BaseModel):
    """
    Récupère la table des matières d'un texte LEGI à partir de son identifiant
    """
    textId: str
    date: str = datetime.now().strftime("%Y-%m-%d")

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/legi/tableMatieres"
        model_reponse = "ConsultTextResponse"


class DossierLegislatifConsult(BaseModel):
    """
    Récupère le contenu d'un dossier législatif à partir de son identifiant
    """
    cid: str
    searchedString: Optional[str] = None

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/dossierLegislatif"
        model_reponse = "ConsultDossierLegislatifResponse"


class SameNumArticle(BaseModel):
    """
    Récupère les articles ayant le même numéro
    """
    textId: str
    articleId: str
    date: str = datetime.now().strftime("%Y-%m-%d")

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/sameNumArticle"
        model_reponse = "SectionsRevisionArticleResponse"


class ConcordanceLinksArticle(BaseModel):
    """
    Récupère les liens de concordance d'un article
    """
    textId: str
    articleId: str
    date: str = datetime.now().strftime("%Y-%m-%d")

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/concordanceLinksArticle"
        model_reponse = "SectionsRevisionArticleResponse"


class ServicePublicLinksArticle(BaseModel):
    """
    Récupère les liens Service-Public.fr d'un article
    """
    textId: str
    articleId: str
    date: str = datetime.now().strftime("%Y-%m-%d")

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/servicePublicLinksArticle"
        model_reponse = "ServicePublicLinksArticleResponse"


class JuriPlanClassement(BaseModel):
    """
    Récupère le plan de classement des jurisprudences
    """
    pass

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/getJuriPlanClassement"
        model_reponse = "GetListPlanClassementJuriResponse"


class GetTables(BaseModel):
    """
    Récupère les tables
    """
    textId: str
    date: str = datetime.now().strftime("%Y-%m-%d")

    class Config:
        """
        Route de la recherche et type de modèle renvoyé
        """
        route = "consult/getTables"
        model_reponse = "GetTableResponse"
