#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 19:09:49 2023

@author: raphael
"""

from datetime import datetime
from models import * 
# Les classes pydantic créées précédemment...

# Création de l'objet
search = SearchRequest(
    fond=Fonds.LODA_DATE,
    recherche=RechercheSpecifiqueDTO(
        secondSort="ID",
        champs=[
            
            ChampDTO(
                criteres = 
                [
                    CritereDTO(
                        proximite=2,
                        valeur="dispositions",
                        criteres=[
                            CritereDTO(
                                typeRecherche=TypeRecherche.UN_DES_MOTS,
                                valeur="soins",
                                operateur=Operateur.ET
                            ),
                            CritereDTO(
                                proximite=3,
                                typeRecherche=TypeRecherche.TOUS_LES_MOTS_DANS_UN_CHAMP,
                                valeur="fonction publique",
                                operateur=Operateur.ET
                            )
                        ],
                        typeRecherche=TypeRecherche.UN_DES_MOTS,
                        operateur=Operateur.ET
                    )
                ],
                typeChamp=TypeChamp.TITLE,
                operateur=Operateur.ET
            )
        ],
        operateur=Operateur.ET,
        filtres=[
            FiltreDTO(
                valeurs=["LOI", "ORDONNANCE", "ARRETE"],
                facette="NATURE"
            ),
            FiltreDTO(
                dates=DatePeriod(
                    end="2016-01-01",
                    start="2016-01-01"
                ),
                facette="DATE_SIGNATURE"
            )
        ],
        fromAdvancedRecherche=False,
        typePagination=TypePagination.DEFAUT,
        pageNumber=1,
        pageSize=10,
        sort="SIGNATURE_DATE_DESC"
    )
)
single_date = datetime.fromtimestamp(1514802418000 / 1000)  # Le timestamp est en millisecondes

recherche_exacte =  SearchRequest(
    fond=Fonds.LODA_DATE,
    recherche=RechercheSpecifiqueDTO(
        champs=[
            ChampDTO(
                typeChamp=TypeChamp.NUM,
                criteres=[
                    CritereDTO(
                        typeRecherche=TypeRecherche.EXACTE,  # A remplacer par EXACTE si vous l'ajoutez dans l'Enum
                        valeur="58-1100",
                        operateur=Operateur.ET
                    )
                ],
                operateur=Operateur.ET
            )
        ],
        filtres=[
            FiltreDTO(
                facette="DATE_VERSION",  # Assurez-vous que cela correspond à une valeur dans l'Enum correspondante
                singleDate="2016-01-01"
            )
        ],
        pageNumber=1,
        pageSize=10,
        sort="PERTINENCE",
        typePagination=TypePagination.DEFAUT
    )
)
search_code = ChampDTO(
        typeChamp=TypeChamp.TITLE,
        criteres=[
            CritereDTO(
                typeRecherche=TypeRecherche.EXACTE,  # A remplacer par EXACTE si vous l'ajoutez dans l'Enum
                valeur="Code de commerce",
                operateur=Operateur.ET
            )
            ]
        )
search_art : ChampDTO(
    typeChamp=TypeChamp.ARTICLE,
    criteres=[
        CritereDTO(
            typeRecherche=TypeRecherche.EXACTE,  # A remplacer par EXACTE si vous l'ajoutez dans l'Enum
            valeur="",
            
        )
        ]
    )
    
recherche_code = RechercheSpecifiqueDTO(
    champs = [search_field]
    
    )




test_search = {
  "fond": "LODA_DATE",
  "recherche": {
    "secondSort": "ID",
    "champs": [
      {
        "criteres": [
          {
            "proximite": 2,
            "valeur": "dispositions",
            "criteres": [
              {
                "typeRecherche": "UN_DES_MOTS",
                "valeur": "soins",
                "operateur": "ET"
              },
              {
                "proximite": "3",
                "typeRecherche": "TOUS_LES_MOTS_DANS_UN_CHAMP",
                "valeur": "fonction publique",
                "operateur": "ET"
              }
            ],
            "typeRecherche": "UN_DES_MOTS",
            "operateur": "ET"
          }
        ],
        "typeChamp": "TITLE",
        "operateur": "ET"
      }
    ],
    "operateur": "ET",
    "filtres": [
      {
        "valeurs": [
          "LOI",
          "ORDONNANCE",
          "ARRETE"
        ],
        "facette": "NATURE"
      },
      {
        "dates": {
          "end": "2018-31-01",
          "start": "2015-01-01"
        },
        "facette": "DATE_SIGNATURE"
      }
    ],
    "fromAdvancedRecherche": False,
    "typePagination": "DEFAUT",
    "pageNumber": 1,
    "pageSize": 10,
    "sort": "SIGNATURE_DATE_DESC"
  }
}
