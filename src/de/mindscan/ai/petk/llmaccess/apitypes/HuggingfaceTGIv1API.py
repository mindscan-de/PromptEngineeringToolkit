'''
Created on 29.09.2024

@author: JohnDoe
'''
from de.mindscan.ai.petk.llmaccess.APIType import APIType

class HuggingfaceTGIv1API(APIType):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__("huggingface_tgi_v1.jsonapi.template", "huggingface-tgi-api-v1", "uuid of 'huggingface-tgi-api-v1'")