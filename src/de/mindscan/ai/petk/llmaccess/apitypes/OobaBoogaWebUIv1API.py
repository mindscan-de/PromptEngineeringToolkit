'''
Created on 22.09.2024

@author: JohnDoe
'''
from de.mindscan.ai.petk.llmaccess.APIType import APIType

class OobaBoogaWebUIv1API(APIType):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__("oobabooga_webui_v1.jsonapi.template", "oobabooga-text-webui-api-v1", "uuid of 'oobabooga-text-webui-api-v1'")


    def getJsonPathQueriesForAnswers(self):
        return {
                "llm.response.content" : "/results/0/text"
            }
    
    def translateFinishReason(self, reason:str):
        return "NONE"