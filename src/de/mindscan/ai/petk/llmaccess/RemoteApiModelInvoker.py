'''
Created on 09.11.2024

@author: JohnDoe
'''
import requests
import json
from jsonpath_ng import parse, jsonpath
import streamlit as st

from de.mindscan.ai.petk.llmaccess.ConnectionEndpoint import ConnectionEndpoint
from de.mindscan.ai.petk.templateegine.AIPETKTemplateEngine import AIPETKTemplateEngine

class RemoteApiModelInvoker(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.template_engine = AIPETKTemplateEngine(None)
        

    def invoke_backend(self, endpoint:ConnectionEndpoint, fully_prepared_llm_query:str):
        completedJsonRequestStructure:str = self.build_json_request_structure(endpoint, fully_prepared_llm_query)
        endpointURL = endpoint.endpoint_url
        
        
        payload = json.loads(completedJsonRequestStructure)
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(endpointURL, json=payload, headers=headers)
        
        if response.status_code!=200:
            return {}
        
        json_answer = json.loads(response.text)
        
        ## TODO: extract unified data from json answer...
        answer_map = self.extract_from_json_map(endpoint.remote_api_type.getJsonPathQueriesForAnswers(), json_answer)
        
        return answer_map

    
    def build_json_request_structure(self, endpoint:ConnectionEndpoint, fully_prepared_llm_query:str) -> str:
        json_api_template:str = endpoint.remote_api_type.getJsonApiTemplate();
        
        # later join with task specific values and also with defaults for this model, and with defaults for this endpoint
        json_api_values = {
            'llm.query':fully_prepared_llm_query
            }
        
        return self.template_engine.evaluateTemplate(json_api_template, json_api_values)

    
    def extract_from_json_map(self, json_path_queries_for_answers, json_answer):
        result = {}
        for key, json_path in json_path_queries_for_answers.items():
            expression = parse(json_path)
            for match in expression.find(json_answer):
                result[key] = match.value
        
        return result
    
    