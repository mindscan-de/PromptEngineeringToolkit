'''
Created on 29.09.2024

@author: JohnDoe
'''
from de.mindscan.ai.petk.llmaccess.APIType import APIType, ANSWER_KEY_CONTENT,\
    ANSWER_KEY_FINISH_REASON, ANSWER_KEY_NUM_GENERATED_TOKENS, ANSWER_KEY_SEED
from de.mindscan.ai.petk.llmaccess.answer.AnswerFinishReason import LM_ANSWER_FINISH_REASON_UNKNOWN,\
    LM_ANSWER_FINISH_REASON_ENDOFSTREAM, LM_ANSWER_FINISH_REASON_TRUNCATED,\
    LM_KEY_FINISH_REASON_DEFAULT

class HuggingfaceTGIv1API(APIType):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__("huggingface_tgi_v1.jsonapi.template", "huggingface-tgi-api-v1", "uuid of 'huggingface-tgi-api-v1'")
        
        
    def getJsonPathQueriesForAnswers(self):
        return {
                ANSWER_KEY_CONTENT : '$.generated_text',
                ANSWER_KEY_FINISH_REASON : '$.details.finish_reason',
                ANSWER_KEY_NUM_GENERATED_TOKENS : '$.details.generated_tokens',
                ANSWER_KEY_SEED : '$.details.seed'
            }
        
    def translateFinishReason(self, reason:str):
        # if we have a finish reason, we may want to translate this reason
        finish_reason = {
            "" : LM_ANSWER_FINISH_REASON_UNKNOWN,
            "unknown" : LM_ANSWER_FINISH_REASON_UNKNOWN,
            "eos_token" : LM_ANSWER_FINISH_REASON_ENDOFSTREAM,
            "length" : LM_ANSWER_FINISH_REASON_TRUNCATED,
            # implement this later
            LM_KEY_FINISH_REASON_DEFAULT : LM_ANSWER_FINISH_REASON_UNKNOWN
            }

        finish_reason.get(reason, None)
        
        
 