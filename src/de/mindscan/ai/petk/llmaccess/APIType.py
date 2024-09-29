'''
Created on 22.09.2024

@author: JohnDoe
'''

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
        pass
    
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