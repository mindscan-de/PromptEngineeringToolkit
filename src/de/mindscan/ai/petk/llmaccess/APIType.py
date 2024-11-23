'''
Created on 22.09.2024

@author: JohnDoe
'''

import os

# Request keys
REQUEST_KEY_LLM_QUERY = "llm.query"

# Answer keys
ANSWER_KEY_CONTENT = "llm.response.content"
ANSWER_KEY_FINISH_REASON = "llm.response.finish.reason"
ANSWER_KEY_NUM_GENERATED_TOKENS = "llm.response.number.generated.tokens"
ANSWER_KEY_SEED = "llm.response.seed"


class APIType(object):
    '''
    classdocs
    '''


    def __init__(self, json_api_template_filename, api_name, api_identifier ):
        '''
        Constructor
        '''
        self.__api_name = api_name
        self.__api_identifier = api_identifier
        self.__json_api_template = self._loadTemplate(json_api_template_filename)
        
    def _loadTemplate(self, template_file_name):
        json_api_template = "unresolved file '"+str(template_file_name)+"'"
        path=os.path.join("../llmaccess/apitypes/",template_file_name)
        is_file = os.path.isfile(path)
        if is_file:
            with open(path,"r") as f:
                json_api_template = str(f.read())
        return json_api_template
    
    def getJsonApiTemplate(self):
        return self.__json_api_template
    
    def getApiName(self):
        return self.__api_name
    
    def getApiIndentifier(self):
        return self.__api_identifier

    ## TODO, should be part of the specializations.
    
    def getJsonPathQueriesForAnswers(self):
        return {}
    
    def translateFinishReason(self, reason:str):
        return {}