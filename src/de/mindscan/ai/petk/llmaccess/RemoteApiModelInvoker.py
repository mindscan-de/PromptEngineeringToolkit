'''
Created on 09.11.2024

@author: JohnDoe
'''
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
        
    def build_json_request_structure(self, endpoint:ConnectionEndpoint, fully_prepared_llm_query:str):
        json_api_template:str = endpoint.remote_api_type.getJsonApiTemplate();
        
        json_api_values = {
            'llm.query':fully_prepared_llm_query
            }
        
        return self.template_engine.evaluateTemplate(json_api_template, json_api_values)
    