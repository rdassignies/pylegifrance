from typing import Optional, ClassVar
from datetime import datetime
from pydantic import BaseModel, Field
import warnings


class BaseConsultModel(BaseModel):
    route: ClassVar[Optional[str]] = None
    model_reponse: ClassVar[Optional[str]] = None


class Jorf(BaseConsultModel):
    """Récupère le contenu d'un texte du fonds JORF à partir de son identifiant"""

    textCid: str
    searchedString: Optional[str] = None
    route = "consult/jorf"
    model_reponse = "ConsultTextResponse"


class LegiPart(BaseConsultModel):
    """Récupère le contenu d'un texte du fonds LEGI à partir de son identifiant et de sa date de vigueur"""

    date: str = datetime.now().strftime("%Y-%m-%d")
    textId: str
    searchedString: Optional[str] = None
    route = "consult/legiPart"
    model_reponse = "ConsultTextResponse"


class GetSectionByCid(BaseConsultModel):
    """Récupère la liste des section par leur identifiant commun"""

    cid: str
    route = "consult/getSectionByCid"


class GetArticle(BaseConsultModel):
    """Récupère un article par son identifiant"""

    id: str
    route = "consult/getArticle"
    model_reponse = "GetArticleResponse"


class GetArticleWithIdEliOrAlias(BaseConsultModel):
    """Récupère un article par son identifiant ELI ou son alias"""

    id: str
    route = "consult/getArticleWithIdEliOrAlias"
    model_reponse = "GetArticleResponse"


class GetArticleByCid(BaseConsultModel):
    """Récupère un article par son identifiant CID"""

    cid: str
    route = "consult/getArticleByCid"
    model_reponse = "GetListArticleResponse"


class CodeConsult(BaseConsultModel):
    """Récupère le contenu d'un code à partir de son identifiant et de sa date de vigueur"""

    date: str = datetime.now().strftime("%Y-%m-%d")
    textId: str
    searchedString: Optional[str] = None
    route = "consult/code"
    model_reponse = "ConsultTextResponse"


class CodeConsultWithAncienId(BaseConsultModel):
    """Récupère le contenu d'un code à partir de son ancien identifiant"""

    ancienId: str
    date: str = datetime.now().strftime("%Y-%m-%d")
    searchedString: Optional[str] = None
    route = "consult/getCodeWithAncienId"
    model_reponse = "ConsultTextResponse"


class CnilConsult(BaseConsultModel):
    """Récupère le contenu d'un texte CNIL à partir de son identifiant"""

    textCid: str
    searchedString: Optional[str] = None
    route = "consult/cnil"
    model_reponse = "ConsultCnilTextResponse"


class CnilConsultWithAncienId(BaseConsultModel):
    """Récupère le contenu d'un texte CNIL à partir de son ancien identifiant"""

    ancienId: str
    searchedString: Optional[str] = None
    route = "consult/getCnilWithAncienId"
    model_reponse = "ConsultCnilTextResponse"


class JuriConsult(BaseConsultModel):
    """Récupère le contenu d'un texte jurisprudentiel à partir de son identifiant"""

    textId: str
    searchedString: Optional[str] = None
    route = "consult/juri"
    model_reponse = "ConsultJuriTextResponse"


class JuriConsultWithAncienId(BaseConsultModel):
    """Récupère le contenu d'un texte jurisprudentiel à partir de son ancien identifiant"""

    ancienId: str
    searchedString: Optional[str] = None
    route = "consult/getJuriWithAncienId"
    model_reponse = "ConsultJuriTextResponse"


class JorfConsult(BaseConsultModel):
    """Récupère le contenu d'un texte du fonds JORF à partir de son identifiant"""

    textCid: str
    searchedString: Optional[str] = None
    route = "consult/jorf"
    model_reponse = "ConsultJorfResponse"


class JorfConsultWithNor(BaseConsultModel):
    """Récupère le contenu d'un texte du fonds JORF à partir de son numéro NOR"""

    nor: str
    searchedString: Optional[str] = None
    route = "consult/getJoWithNor"
    model_reponse = "ConsultJorfResponse"


class JorfContConsult(BaseConsultModel):
    """Récupère le contenu d'un JO à partir de son identifiant"""

    contId: str
    searchedString: Optional[str] = None
    route = "consult/jorfCont"
    model_reponse = "GetJosResponse"


class LastNJo(BaseConsultModel):
    """Récupère les N derniers JO"""

    n: int = Field(..., description="Nombre de JO à récupérer")
    route = "consult/lastNJo"
    model_reponse = "GetJorfContResponse"


class KaliTextConsult(BaseConsultModel):
    """Récupère le contenu d'un texte KALI à partir de son identifiant"""

    textId: str
    searchedString: Optional[str] = None
    route = "consult/kaliText"
    model_reponse = "ConsultKaliTextResponse"


class KaliTextConsultArticle(BaseConsultModel):
    """Récupère un article d'un texte KALI à partir de son identifiant"""

    textId: str
    articleId: str
    searchedString: Optional[str] = None
    route = "consult/kaliArticle"
    model_reponse = "ConsultKaliTextResponse"


class KaliTextConsultSection(BaseConsultModel):
    """Récupère une section d'un texte KALI à partir de son identifiant"""

    textId: str
    sectionId: str
    searchedString: Optional[str] = None
    route = "consult/kaliSection"
    model_reponse = "ConsultKaliTextResponse"


class KaliContConsult(BaseConsultModel):
    """Récupère le contenu d'un conteneur KALI à partir de son identifiant"""

    contId: str
    searchedString: Optional[str] = None
    route = "consult/kaliCont"
    model_reponse = "ConsultKaliContResponse"


class KaliContConsultIdcc(BaseConsultModel):
    """Récupère le contenu d'un conteneur KALI à partir de son IDCC"""

    idcc: str
    searchedString: Optional[str] = None
    route = "consult/kaliContIdcc"
    model_reponse = "ConsultKaliContResponse"


class LegiSommaireConsult(BaseConsultModel):
    """Récupère la table des matières d'un texte LEGI à partir de son identifiant"""

    textId: str
    date: str = datetime.now().strftime("%Y-%m-%d")
    route = "consult/legi/tableMatieres"
    model_reponse = "ConsultTextResponse"


class DossierLegislatifConsult(BaseConsultModel):
    """Récupère le contenu d'un dossier législatif à partir de son identifiant"""

    cid: str
    searchedString: Optional[str] = None
    route = "consult/dossierLegislatif"
    model_reponse = "ConsultDossierLegislatifResponse"


class SameNumArticle(BaseConsultModel):
    """Récupère les articles ayant le même numéro"""

    textId: str
    articleId: str
    date: str = datetime.now().strftime("%Y-%m-%d")
    route = "consult/sameNumArticle"
    model_reponse = "SectionsRevisionArticleResponse"


class ConcordanceLinksArticle(BaseConsultModel):
    """Récupère les liens de concordance d'un article"""

    textId: str
    articleId: str
    date: str = datetime.now().strftime("%Y-%m-%d")
    route = "consult/concordanceLinksArticle"
    model_reponse = "SectionsRevisionArticleResponse"


class ServicePublicLinksArticle(BaseConsultModel):
    """Récupère les liens Service-Public.fr d'un article"""

    textId: str
    articleId: str
    date: str = datetime.now().strftime("%Y-%m-%d")
    route = "consult/servicePublicLinksArticle"
    model_reponse = "ServicePublicLinksArticleResponse"


class JuriPlanClassement(BaseConsultModel):
    """Récupère le plan de classement des jurisprudences"""

    route = "consult/getJuriPlanClassement"
    model_reponse = "GetListPlanClassementJuriResponse"


class GetTables(BaseConsultModel):
    """Récupère les tables"""

    textId: str
    date: str = datetime.now().strftime("%Y-%m-%d")
    route = "consult/getTables"
    model_reponse = "GetTableResponse"


class CodeTableMatieres(BaseConsultModel):
    """
    Récupère la table des matières d'un texte de type CODE à partir de son identifiant et de sa date de vigueur
    DEPRECATED: Cette route est dépréciée. Utilisez LegiSommaireConsult avec le paramètre nature='CODE' à la place.
    """

    textId: str
    date: str = datetime.now().strftime("%Y-%m-%d")

    def __init__(self, **data):
        super().__init__(**data)
        warnings.warn(
            "La route 'consult/code/tableMatieres' est dépréciée. "
            "Utilisez LegiSommaireConsult avec le paramètre nature='CODE' à la place.",
            DeprecationWarning,
            stacklevel=2,
        )

    route = "consult/code/tableMatieres"
    model_reponse = "ConsultTextResponse"
