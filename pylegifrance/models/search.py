#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 19:16:30 2023
Modèles pydantic pour la recherche (route: "search") de l'API Legifrance
@author: Raphaël d'Assignies'
"""

from typing import List, Union, Optional, ClassVar
from enum import Enum
from datetime import datetime


from pydantic import BaseModel, field_validator
from pylegifrance.models.constants import (
    Fonds,
    TypeFacettes,
    TypeRecherche,
    CodeNom,
    Nature,
)

from pylegifrance.models.constants import Operateur, TypeChamp


# Champs autorisés pour CODE, LODA, JURI,...


class ChampsCODE(Enum):
    ALL = "ALL"
    TITLE = "TITLE"
    TABLE = "TABLE"
    NUM_ARTICLE = "NUM_ARTICLE"
    ARTICLE = "ARTICLE"


class ChampsLODA(Enum):
    ALL = "ALL"
    TITLE = "TITLE"
    TABLE = "TABLE"
    NOR = "NOR"
    NUM = "NUM"
    NUM_ARTICLE = "NUM_ARTICLE"
    ARTICLE = "ARTICLE"
    VISA = "VISA"
    NOTICE = "NOTICE"
    VISA_NOTICE = "VISA_NOTICE"
    TRAVAUX_PREP = "TRAVAUX_PREP"
    SIGNATURE = "SIGNATURE"
    NOTA = "NOTA"


class ChampsJURI(Enum):
    ALL = "ALL"
    TITLE = "TITLE"
    ABSTRAT = "ABSTRAT"
    TEXTE = "TEXTE"
    RESUMES = "RESUMES"
    NUM_AFFAIRE = "NUM_AFFAIRE"


# Facettes autorisées pour CODE, LODA ...


class FacettesCODE(Enum):
    NOM_CODE = "NOM_CODE"
    DATE_SIGNATURE = "DATE_SIGNATURE"
    DATE_VERSION = "DATE_VERSION"


class FacettesLODA(Enum):
    NATURE = "NATURE"
    NOR = "NOR"
    DATE_VERSION = "DATE_VERSION"
    DATE_SIGNATURE = "DATE_SIGNATURE"
    TEXT_LEGAL_STATUS = "TEXT_LEGAL_STATUS"
    ARTICLE_LEGAL_STATUS = "ARTICLE_LEGAL_STATUS"


# Criteres et champ génériques


class Critere(BaseModel):
    """
    Liste des critères/groupes de critères de recherche pour ce champ
    """

    typeRecherche: TypeRecherche = TypeRecherche.EXACTE
    valeur: str  # " Mot(s)/expression recherchés"
    operateur: Operateur = Operateur.ET


class Champ(BaseModel):
    """
    Modèle décrivant une recherche dans un champ spécifique
    """

    typeChamp: TypeChamp
    criteres: List[Critere]
    operateur: Operateur = Operateur.ET


# Modèle de filtres spécifiques


class DateVersionFiltre(BaseModel):
    facette: TypeFacettes = TypeFacettes.DATE_VERSION
    singleDate: str = datetime.now().strftime("%Y-%m-%d")


class DatesPeriod(BaseModel):
    start: Optional[str]
    end: Optional[str] = None

    @field_validator("start", "end")
    @classmethod
    def valider_format_date(cls, v):
        if v is None:
            return v
        try:
            # Valider et convertir la date en utilisant le format YYYY-DD-MM
            return datetime.strptime(v, "%Y-%m-%d").date().strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Le format de la date doit être YYYY-MM-DD")


class DateSignatureFiltre(BaseModel):
    facette: TypeFacettes = TypeFacettes.DATE_SIGNATURE
    dates: DatesPeriod


class NomCodeFiltre(BaseModel):
    facette: TypeFacettes = TypeFacettes.NOM_CODE
    valeurs: List[Union[CodeNom, str]]

    @field_validator("valeurs")
    @classmethod
    def validate_code_names(cls, v):
        """
        Validates and converts string code names to CodeNom enum values if needed.
        This maintains backward compatibility with code that passes strings.
        Raises ValidationError if a string is not a valid code name.
        """
        result = []
        for code in v:
            if isinstance(code, str):
                # Check if the string is a direct enum value (e.g., "CCIV")
                if code in CodeNom.__members__:
                    result.append(CodeNom[code])
                else:
                    # Check if the string is a value of an enum (e.g., "Code civil")
                    found = False
                    for enum_val in CodeNom:
                        if enum_val.value == code:
                            result.append(enum_val)
                            found = True
                            break
                    if not found:
                        # If not found, raise a ValidationError
                        raise ValueError(f"Invalid code name: {code}")
            else:
                result.append(code)
        return result


class NatureFiltre(BaseModel):
    facette: TypeFacettes = TypeFacettes.NATURE
    valeurs: List[Nature] = [
        Nature.LOI,
        Nature.ORDONNANCE,
        Nature.DECRET,
        Nature.ARRETE,
    ]


class EtatTextFiltre(BaseModel):
    facette: TypeFacettes = TypeFacettes.TEXT_LEGAL_STATUS
    valeur: str = "VIGUEUR"


class EtatArticleFiltre(BaseModel):
    facette: TypeFacettes = TypeFacettes.ARTICLE_LEGAL_STATUS
    valeur: str = "VIGUEUR"


class Recherche(BaseModel):
    """Modèle pour créer une recherche dans les différents fonds accessibles depuis
    l'API Legifrance

    Args:
    * secondSort (Optional[str], default=None): Tri des éléments trouvés (Les tris possibles dépendent du fonds recherché)
    champs (List[ChampDTO]): List of fields to search for.
    filters (Optional[List[FiltreDTO]], default=None): List of filters to apply to the search.
    * fromAdvancedRecherche (Optional[bool], default=None): Déterminer s'il s'agit d'une recherche avancée
    typePagination (TypePagination): Type de pagination. Spécifique pour les recherches dans les articles d'un texte, dans les autres cas la valeur sera toujours DEFAULT. Lors de la navigation dans plusieurs pages, il est nécessaire de passer la valeur reçue dans la réponse précédente.
    pageNumber (int):Numéro de la page à consulter
    pageSize (int): Nombre de résultat(s) par page
    sort (str): Tri des éléments trouvés (Les tris possibles dépendent du fonds recherché)

    * * Non implémenté pour le moment
    """

    champs: List[Champ]
    filtres: List[
        Union[
            NomCodeFiltre,
            DateVersionFiltre,
            NatureFiltre,
            EtatTextFiltre,
            EtatArticleFiltre,
            DateSignatureFiltre,
        ]
    ]
    pageNumber: int = 1
    pageSize: int = 10
    operateur: Operateur = Operateur.ET
    sort: str = "PERTINENCE"
    typePagination: str = "ARTICLE"

    # TODO : ajouter un validateur pour page_size, max 100


class Fond(BaseModel):
    fond: Fonds


class RechercheFinal(BaseModel):
    """
    Final aggregated model for searching

    """

    fond: Fonds
    recherche: Recherche  # Défini ailleurs

    route: ClassVar[str] = "search"
    model_reponse: ClassVar[str] = "SearchResponseDTO"

    @field_validator("recherche")
    @classmethod
    def validate_champs(cls, v, info):
        """
        Validates the compatibility between the field type and the archive fonds.
        The test relies on an ENUM list of fields authorized for each fonds.
        """
        fond = info.data.get("fond")
        for champ in v.champs:
            if fond in [Fonds.CODE_DATE, Fonds.CODE_ETAT]:
                if champ.typeChamp.value not in ChampsCODE.__members__:
                    raise ValueError(
                        f"TypeChamp {champ.typeChamp} is not valid for the fond {fond}"
                    )
            if fond in [Fonds.LODA_DATE, Fonds.LODA_ETAT]:
                if champ.typeChamp.value not in ChampsLODA.__members__:
                    raise ValueError(
                        f"TypeChamp {champ.typeChamp} is not valid for the fond {fond}"
                    )
            if fond in [Fonds.JURI]:
                if champ.typeChamp.value not in ChampsJURI.__members__:
                    raise ValueError(
                        f"TypeChamp {champ.typeChamp} is not valid for the fond {fond}"
                    )
        return v

    @field_validator("recherche")
    @classmethod
    def validate_filtres(cls, v, info):
        """
        Validates the compatibility between the filter type (facet)
        and the archive fonds.The test is based on an ENUM list of facet names
        authorized for each fonds.
        """
        fond = info.data.get("fond")
        for filtre in v.filtres:
            if fond in [Fonds.CODE_DATE, Fonds.CODE_ETAT]:
                if filtre.facette.value not in FacettesCODE.__members__:
                    raise ValueError(
                        f"Facet {filtre.facette} "
                        f"is not valid for the fond {fond}"
                        f" - allowed facets : {FacettesCODE.__members__}"
                    )
            if fond in [Fonds.LODA_DATE, Fonds.LODA_ETAT]:
                if filtre.facette.value not in FacettesLODA.__members__:
                    raise ValueError(
                        f"Facet {filtre.facette} "
                        f"is not valid for the fond {fond}"
                        f" - allowed facets : {FacettesLODA.__members__}"
                    )
        return v
