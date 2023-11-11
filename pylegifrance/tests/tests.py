#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 12:39:06 2023

@author: raphael
"""

import inspect
from typing import Optional
from types import MethodType
import inspect
from inspect import Parameter

from functools import partial
from types import MethodType
from pydantic import BaseModel, Field
from typing import Optional
import inspect

class JorfModel(BaseModel):
    route: str = "/consult/jorf"
    textCid: str
    champs_2: str
    searchedString: Optional[str] = None
    
class test(BaseModel):
    route: str = "/test"
    _id: str



class MaClasse:
   
    def __init__(self):
        import models
        for name, cls in inspect.getmembers(models):
            if inspect.isclass(cls) and issubclass(cls, BaseModel):
                dummy_instance = cls(**{field: "dummy" for field in cls.__annotations__ if field != "route"})
                if hasattr(dummy_instance, "route"):
                    route = getattr(dummy_instance, "route")
                    method_name = route.replace("/", "_").replace(":", "_")
                    dynamic_method = self.make_method(cls)
                    setattr(self, method_name, MethodType(dynamic_method, self))
                    
    
    @staticmethod          
    def make_method(cls):
        def dynamic_method(self, **kwargs):
            # instanciation du modèle Pydantic avec les arguments
            model_instance = cls(**kwargs)
            # accès aux attributs du modèle
            route = model_instance.route
            print(f"Route: {route}. Appelée avec les arguments valides : {kwargs}")
        
        params = [
            Parameter(name, Parameter.KEYWORD_ONLY, default=(Parameter.empty if typ == str else None), annotation=typ)
            for name, typ in cls.__annotations__.items() if name != "route"
        ]
        print(params)
        dynamic_method.__signature__ = inspect.Signature(params)
        print(dynamic_method.__signature__)
        dynamic_method.__doc__ = f"Appelle l'API avec les données suivantes : {dynamic_method.__signature__ }"

        return dynamic_method
        


# Test
struct =   {
   
   "textCid": "JORFTEXT000033736934",
   "champs_2" : 'rR',
   "searchedString": "constitution 1958"
   }


ma_classe = MaClasse()
