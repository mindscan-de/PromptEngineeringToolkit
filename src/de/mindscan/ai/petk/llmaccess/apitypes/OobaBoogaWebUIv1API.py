'''
Created on 22.09.2024

@author: JohnDoe
'''
from de.mindscan.ai.petk.llmaccess.APIType import APIType, ANSWER_KEY_CONTENT
from de.mindscan.ai.petk.llmaccess.answer.AnswerFinishReason import LM_ANSWER_FINISH_REASON_NONE,\
    LM_ANSWER_FINISH_REASON_UNKNOWN, LM_KEY_FINISH_REASON_DEFAULT

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
                ANSWER_KEY_CONTENT : '$.results[0].text'
            }
    
    def getFinishReasonTranslationMap(self):
        return {
            LM_KEY_FINISH_REASON_DEFAULT : LM_ANSWER_FINISH_REASON_UNKNOWN
            }
        