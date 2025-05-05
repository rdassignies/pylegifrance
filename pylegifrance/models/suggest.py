from typing import List
from enum import Enum


from pydantic import BaseModel, Field, ConfigDict


# SUGGEST CONTROLLER


# Liste des fonds dans lesquels exécuter la recherche pour la suggestion
class SupplyEnum(str, Enum):
    ALL = "ALL"
    ALL_SUGGEST = "ALL_SUGGEST"
    LODA_LIST = "LODA_LIST"
    CODE_LIST = "CODE_LIST"
    CODE_RELEASE_DATE = "CODE_RELEASE_DATE"
    CODE_RELEASE_DATE_SUGGEST = "CODE_RELEASE_DATE_SUGGEST"
    CODE_LEGAL_STATUS = "CODE_LEGAL_STATUS"
    LODA_RELEASE_DATE = "LODA_RELEASE_DATE"
    LODA_RELEASE_DATE_SUGGEST = "LODA_RELEASE_DATE_SUGGEST"
    LODA_LEGAL_STATUS = "LODA_LEGAL_STATUS"
    KALI = "KALI"
    KALI_TEXT = "KALI_TEXT"
    CONSTIT = "CONSTIT"
    CETAT = "CETAT"
    JUFI = "JUFI"
    JURI = "JURI"
    JORF = "JORF"
    JORF_SUGGEST = "JORF_SUGGEST"
    CNIL = "CNIL"
    ARTICLE = "ARTICLE"
    CIRC = "CIRC"
    ACCO = "ACCO"
    PDF = "PDF"


class SuggestSupplyRequest(BaseModel):
    """Requête de suggestion d'une recherche textuelle dans un ou
    plusieurs fonds
    """

    searchText: str = Field(..., example="mariage", description="Texte à rechercher")
    supplies: List[SupplyEnum] = Field(
        ...,
        example=["JORF", "JURI"],
        description="Liste des fonds dans lesquels exécuter la recherche pour la suggestion",
    )
    documentsDits: bool = Field(
        True, description="Indicateur de la présence de documents dits"
    )

    model_config = ConfigDict(route="suggest")


CODE_LIST = {
    "CCIV": "Code civil",
    "CPRCIV": "Code de procédure civile",
    "CCOM": "Code de commerce",
    "CTRAV": "Code du travail",
    "CPI": "Code de la propriété intellectuelle",
    "CPEN": "Code pénal",
    "CPP": "Code de procédure pénale",
    "CASSUR": "Code des assurances",
    "CCONSO": "Code de la consommation",
    "CSI": "Code de la sécurité intérieure",
    "CSP": "Code de la santé publique",
    "CSS": "Code de la sécurité sociale",
    "CESEDA": "Code de l'entrée et du séjour des étrangers et du droit d'asile",
    "CGCT": "Code général des collectivités territoriales",
    "CPCE": "Code des postes et des communications électroniques",
    "CENV": "Code de l'environnement",
    "CJA": "Code de justice administrative",
}
