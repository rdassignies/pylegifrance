from typing import Optional, List, Dict
import re
from enum import Enum
from datetime import datetime


from pydantic import BaseModel, Field, validator
from inspect import Signature, Parameter

class JorfModel(BaseModel):
    textCid:str = "JORFTEXT000033736934"
    searchedString: Optional[str] = None

    class Config:
        route = "consult/jorf"


class LegiPart(BaseModel):
    date: str = "2021-04-15"
    textId: str = "LEGITEXT000006075116"
    searchedString: Optional[str] = None

    class Config:
        route = "consult/legiPart"




class Fonds(str, Enum):
    JORF = "JORF"
    CNIL = "CNIL"
    CETAT = "CETAT"
    JURI = "JURI"
    JUFI = "JUFI"
    CONSTIT = "CONSTIT"
    KALI = "KALI"
    CODE_DATE = "CODE_DATE"
    CODE_ETAT = "CODE_ETAT"
    LODA_DATE = "LODA_DATE"
    LODA_ETAT = "LODA_ETAT"
    ALL = "ALL"
    CIRC = "CIRC"
    ACCO = "ACCO"

class RechercheFonds(BaseModel):
    fonds: Fonds
    
class Operateur(Enum):
    """
    Opérateur entre les champs de recherche

    """
    ET = "ET"
    OU = "OU"

class TypeRecherche(Enum):
    EXACTE = "EXACTE"
    UN_DES_MOTS = "UN_DES_MOTS"
    TOUS_LES_MOTS_DANS_UN_CHAMP = "TOUS_LES_MOTS_DANS_UN_CHAMP"
    AUCUN_DES_MOTS = "AUCUN_DES_MOTS"
    AUCUNE_CORRESPONDANCE_A_CETTE_EXPRESSION = "AUCUNE_CORRESPONDANCE_A_CETTE_EXPRESSION"

class TypeChamp(Enum):
    ALL = "ALL"
    TITLE = "TITLE"
    TABLE = "TABLE"
    NOR = "NOR"
    NUM = "NUM"
    ADVANCED_TEXTE_ID = "ADVANCED_TEXTE_ID"
    NUM_DELIB = "NUM_DELIB"
    NUM_DEC = "NUM_DEC"
    NUM_ARTICLE = "NUM_ARTICLE"
    ARTICLE = "ARTICLE"
    MINISTERE = "MINISTERE"
    VISA = "VISA"
    NOTICE = "NOTICE"
    VISA_NOTICE = "VISA_NOTICE"
    TRAVAUX_PREP = "TRAVAUX_PREP"
    SIGNATURE = "SIGNATURE"
    NOTA = "NOTA"
    NUM_AFFAIRE = "NUM_AFFAIRE"
    ABSTRATS = "ABSTRATS"
    RESUMES = "RESUMES"
    TEXTE = "TEXTE"
    ECLI = "ECLI"
    NUM_LOI_DEF = "NUM_LOI_DEF"
    TYPE_DECISION = "TYPE_DECISION"
    NUMERO_INTERNE = "NUMERO_INTERNE"
    REF_PUBLI = "REF_PUBLI"
    RESUME_CIRC = "RESUME_CIRC"
    TEXTE_REF = "TEXTE_REF"
    TITRE_LOI_DEF = "TITRE_LOI_DEF"
    RAISON_SOCIALE = "RAISON_SOCIALE"
    MOTS_CLES = "MOTS_CLES"
    IDCC = "IDCC"

class CritereDTO(BaseModel):
    proximite: Optional[int]
    valeur: str
    criteres: Optional[List["CritereDTO"]] = [] #Sous-critère/Sous-groupe de critères
    typeRecherche: TypeRecherche
    operateur: Optional[Operateur]

class ChampDTO(BaseModel):
    """ Objet décrivant une recherche dans un champ spécifique
    
    """
    criteres: List[CritereDTO]
    typeChamp: TypeChamp
    operateur: Optional[Operateur] = None


CritereDTO.update_forward_refs()


class TypePagination(Enum):
    DEFAUT = "DEFAUT"
    ARTICLE = "ARTICLE"

class DatePeriod(BaseModel):
    end: Optional[str] = None
    start: Optional[str] = None
      
    @validator('end', 'start')
    def check_date_format(cls, v):
        if v is not None:
            if not re.match(r'\d{4}-\d{2}-\d{2}', v):
                raise ValueError('singleDate must be in YYYY-MM-DD format')
        return v
    

class FiltreDTO(BaseModel):
    """
    Objet décrivant un filtre de recherche


    """
    valeurs: Optional[List[str]] = None
    multiValeurs: Optional[Dict[str, List[str]]] = None #Map des sous-valeur d'une valeur de filtre dans le cas d'un filtre par option texte. La clé doit être la valeur correspondante au parent dans la liste 'valeurs'
    dates: Optional[DatePeriod] = None
    facette: str
    singleDate: Optional[str] = None
    
    @validator('singleDate')
    def check_date_format(cls, v):
        if v is not None:
            if not re.match(r'\d{4}-\d{2}-\d{2}', v):
                raise ValueError('singleDate must be in YYYY-MM-DD format')
        return v

class RechercheSpecifiqueDTO(BaseModel):
    """ Objet permettant de créer une recherche
    Args:
        secondSort (Optional[str], default=None): Tri des éléments trouvés. Les tris possibles dépendent du fonds recherché.
        champs (List[ChampDTO]): Liste des champs à rechercher.
        filtres (Optional[List[FiltreDTO]], default=None): Liste des filtres à appliquer à la recherche.
        fromAdvancedRecherche (Optional[bool], default=None): Indique si la recherche provient d'une recherche avancée.
        typePagination (TypePagination): Type de pagination à utiliser pour la recherche.
        pageNumber (int): Numéro de la page à récupérer.
        pageSize (int): Nombre d'éléments par page.
        sort (str): Champ sur lequel trier les résultats de la recherche.

    """
    secondSort:Optional[str] = Field(None, description="Tri des éléments trouvés (Les tris possibles dépendent du fonds recherché)")
    champs: List[ChampDTO]
    filtres: Optional[List[FiltreDTO]] = None
    fromAdvancedRecherche: Optional[bool] = None
    typePagination: TypePagination
    pageNumber: int
    pageSize: int
    sort: str

class SearchRequest(BaseModel):
    """Requête paginée de recherche """
    fond: Fonds
    recherche: RechercheSpecifiqueDTO
    
class Recherche(BaseModel) : 
    """Requête de recherche porteur du/des fonds ciblés, des filtres et des informations de pagination
    """

    recherche: SearchRequest
    
    
endpoints = {
    "consult/jorf": JorfModel,
    "consult/legiPart": LegiPart,
    "search" : Recherche, 
}







