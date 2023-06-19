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
      }, 
      "/consult/juri": 
      {
       "textId": "JURITEXT000037999394",
       "searchedString": "constitution 1958"
       }, 
      "/consult/jorf" : 
      {
       "textCid": "JORFTEXT000033736934",
       "searchedString": "constitution 1958"
       },
      "/list/dossiersLegislatifs" : 
         {
             "legislatureId": 15,
             "type": "LOI_PUBLIEE"
         },
    "/suggest" : 
        {
            "supplies": [
                "JORF",
                "JURI"
        ],
        "searchText": "mariage"
        }
        
    }

