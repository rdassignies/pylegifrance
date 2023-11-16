#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 19:16:30 2023

@author: raphael
"""

from typing import List, Union, Optional, Dict, Any
from enum import Enum
from datetime import datetime, date


from pydantic import BaseModel, field_validator
from models.generic import (Operateur, TypeChamp, 
                            Fonds,  TypeFacettes, TypeRecherche, 
                            CodeNom, 
                            )

# Champs autorisés pour CODE, LODA, ... 
# TODO: sortir ces infos pour les mettre dans un fichier spécifique

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

# Facettes autorisées pour CODE, LODA ... 
class FacettesCODE(Enum):
    NOM_CODE = "NOM_CODE"
    DATE_SIGNATURE = "DATE_SIGNATURE"
    DATE_VERSION = "DATE_VERSION"
    etatTexte = "etatTexte"

class FacettesLODA(Enum) : 
    NATURE = "NATURE"
    NOR = "NOR"
    DATE_VERSION = "DATE_VERSION"
    TEXT_LEGAL_STATUS = "TEXT_LEGAL_STATUS"


class Critere(BaseModel):
    """
    Critère(s) de recherche associés à un champ
    """
    
    #criteres: Optional[List["Critere"]] = [] #Sous-critère/Sous-groupe de critères
    typeRecherche: TypeRecherche = "EXACTE"
    valeur: str
    operateur: Operateur = "ET"

class Champ(BaseModel):
    """
    Objet décrivant une recherche dans un champ spécifique
    """
    typeChamp: TypeChamp
    criteres: List[Critere]
    operateur: Operateur = Operateur.ET


# Modèle de filtres spécifiques

class DateVersionFiltre(BaseModel):
    facette:TypeFacettes = TypeFacettes.DATE_VERSION
    singleDate:str = datetime.now().strftime("%Y-%m-%d")

class NomCodeFiltre(BaseModel):
    facette:TypeFacettes = TypeFacettes.NOM_CODE
    valeurs:List[CodeNom]
    
class NatureFiltre(BaseModel): 
    facette:TypeFacettes = TypeFacettes.NATURE
    valeurs:str=None

class EtatFiltre(BaseModel) : 
    facette:TypeFacettes = TypeFacettes.TEXT_LEGAL_STATUS
    valeur:str="VIGUEUR"


class Recherche(BaseModel):
    """ Modèle permettant de créer une recherche. Le fond est ajouté par la suite. 
    * Non implémenté pour le moment
    Args:
        * secondSort (Optional[str], default=None): Tri des éléments trouvés. Les tris possibles dépendent du fonds recherché.
        champs (List[ChampDTO]): Liste des champs à rechercher.
        filtres (Optional[List[FiltreDTO]], default=None): Liste des filtres à appliquer à la recherche.
        * fromAdvancedRecherche (Optional[bool], default=None): Indique si la recherche provient d'une recherche avancée.
        typePagination (TypePagination): Type de pagination à utiliser pour la recherche.
        pageNumber (int): Numéro de la page à récupérer.
        pageSize (int): Nombre d'éléments par page.
        sort (str): Champ sur lequel trier les résultats de la recherche.
    
    * Non implémenté pour le moment
    """
    champs: List[Champ]
    filtres: List[Union[NomCodeFiltre, 
                        DateVersionFiltre, 
                        NatureFiltre, 
                        EtatFiltre]]
    pageNumber: int=1
    pageSize: int=10
    operateur: str = Operateur.ET
    sort: str = "PERTINENCE"
    typePagination: str = "ARTICLE"
    
    # TODO : ajouter un validateur pour page_size, max 100

class RechercheFinal(BaseModel):
    """
    Modèle aggrégé final pour la recherche dans un fond spécifique
    
    """
    fond:Fonds
    recherche: Recherche  # Défini ailleurs
    
    class Config:
        """ 
        Route de la recherche et typ
        """
        route = "search"
        model_reponse="SearchResponseDTO"
    
   
    @field_validator('recherche')
    @classmethod
    def validate_champs(cls, v, values): 
        """
        Valide la compatibilité entre le type de champ et le fond. 
        Le test s'appuie sur une list ENUM des champs autorisés par fond

        """
        fond = values.data['fond']
        for champ in v.champs : 
            if fond in ['CODE_DATE', 'CODE_ETAT']:
               if champ.typeChamp.value not in ChampsCODE.__members__ : 
                   raise ValueError(f"TypeChamp {champ.typeChamp} n'est pas valide pour le fond {fond}")
            if fond in ['LODA_DATE', 'LODA_ETAT']:
               if champ.typeChamp.value not in ChampsLODA.__members__ : 
                   raise ValueError(f"TypeChamp {champ.typeChamp} n'est pas valide pour le fond {fond}")

        return v

    @field_validator('recherche')
    @classmethod
    def validate_filtres(cls, v, values):
        """
        Valide la compatibilité entre le type de filtre(facette) et le fond. 
        Le test s'appuie sur une list ENUM des noms de facettes autorisés par fond

        """
        fond = values.data['fond']
        for filtre in v.filtres : 
            if fond in ['CODE_DATE', 'CODE_ETAT']:
               if filtre.facette.value not in FacettesCODE.__members__ : 
                   raise ValueError(f"La facette {filtre.facette} n'est pas valide pour le fond {fond}"
                                    f" - facettes autorisées : {FacettesLODA.__members__}")
            if fond in ['LODA_DATE', 'LODA_ETAT']:
               if filtre.facette.value not in FacettesLODA.__members__ : 
                   raise ValueError(f"La facette {filtre.facette} n'est pas valide pour le fond {fond}"
                                    f" - facettes autorisées : {FacettesLODA.__members__}")
             
        return v
