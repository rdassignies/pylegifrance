#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:14:21 2023

@author: raphael
"""
 
routes = {
      "/consult/sameNumArticle": {
        "textCid": "",
        "articleCid": "",
        "date": "",
        "articleNum": ""
      },
      "/consult/legiPart": {
        "searchedString": "",
        "date": "",
        "textId": ""
      }
    }

liste_code = {
  "route" : "list/code",
      'payload' : {
      "states": [
        "VIGUEUR",
        "ABROGE",
        "VIGUEUR_DIFF"
      ],
      "pageNumber": 1,
      "pageSize": 10,
      "codeName": "Code de la propriété intellectuelle",
      "sort": "TITLE_ASC"
    }
  }
  
numero = "2019-290"

txt_complet_recup_identifiant = {
    "recherche": {
        "champs": [
            {
                "typeChamp": "NUM",
                "criteres": [
                    {
                        "typeRecherche": "EXACTE",
                        "valeur": f"{numero}",
                        "operateur": "ET"
                    }
                ],
                "operateur": "ET"
            }
        ],
       "filtres": [
            {
                "facette": "DATE_VERSION",
                "singleDate": 1561132975000
            },
            {
                "facette": "TEXT_LEGAL_STATUS",
                "valeur": "VIGUEUR"
            }
        ],
        "pageNumber": 1,
        "pageSize": 10,
        "operateur": "ET",
    "sort": "PERTINENCE",
        "typePagination": "DEFAUT"
    },
   "fond": "LODA_ETAT"
}

code_complet = {
    "recherche": {
        "champs": [
            {
                "typeChamp": "ALL",
                "criteres": [
                    {
                        "typeRecherche": "EXACTE",
                        "valeur": "Fouille",
                        "operateur": "ET"
                    }
                ],
                "operateur": "ET"
            }
        ],
       "filtres": [
	       
           
            {
                "facette": "TEXT_LEGAL_STATUS",
                "valeur": "VIGUEUR"
            }
        ],
        "pageNumber": 1,
        "pageSize": 10,
        "operateur": "ET",
    "sort": "PERTINENCE",
        "typePagination": "DEFAUT"
    },
   "fond": "LODA_ETAT"
}

table_matiere = {
    
  "nature": "CODE",
  "textId": "LEGITEXT000006071366",
  "date": "2021-04-15"
}

recup_loi_identifiant =  {
  "date": 1561132975000,
  "textId": "LEGITEXT000038359719"
  }

list_dossiers_legis = {
  "legislatureId": 15,
  "type": "LOI_PUBLIEE"
}

list_code = {
  "states": [
    "VIGUEUR",
    "ABROGE",
    "VIGUEUR_DIFF"
  ],
  "pageNumber": 1,
  "pageSize": 10,
  "codeName": "Code civil",
  "sort": "TITLE_ASC"
}

consult_code = {
  "textId": "LEGITEXT000006075116",
  "searchedString": "constitution 1958",
  "date": "2021-04-15",
  "sctCid": "LEGISCTA000006112861"
}