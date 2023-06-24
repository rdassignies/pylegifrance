#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from pydantic import BaseModel
from inspect import Signature, Parameter

import models



def _create_function_from_pydantic_model(model: BaseModel):
    
    parameters = [Parameter(name, Parameter.KEYWORD_ONLY, annotation=annotation)
                  for name, annotation in model.__annotations__.items()]
    
    parameters.append(Parameter('route', Parameter.KEYWORD_ONLY, default=model.Config.route))
    
    signature = Signature(parameters)
    
    print(signature)
     
    def func(*args, **kwargs):
        bound_values = signature.bind(*args, **kwargs)
        arguments = bound_values.arguments
        print(arguments)
        
    
    func.__signature__ = signature
    func.__annotations__ = {'return': dict}
    func.__doc__ = f"Appelle l'API avec les données suivantes : {func.__signature__ }"
    
    return func

def create_endpoints() : 
    endpoints = {}

    for name in dir(models):
        attribute = getattr(models, name)
        if isinstance(attribute, type) and issubclass(attribute, BaseModel) and attribute != BaseModel:
           route = getattr(attribute.Config, 'route', None)
           route = route.replace("/", "_")
           
           if route is not None:
               
                endpoints[route] = _create_function_from_pydantic_model(attribute)
    return endpoints