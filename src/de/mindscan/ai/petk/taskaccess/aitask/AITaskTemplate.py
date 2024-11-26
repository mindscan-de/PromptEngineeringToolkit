'''
Created on 26.11.2024

@author: JohnDoe
'''

class AITaskTemplate(object):
    '''
    classdocs
    '''


    def __init__(self, name, model_compatibility, system_prompt, task_query):
        '''
        Constructor
        '''
        self.__template_name= name
        self.__model_compatibility = model_compatibility
        self.__systemprompt = system_prompt
        self.__task_query = task_query
        
    def get_systemm_prompt(self):
        return self.__systemprompt
        
    def get_template_name(self):
        return self.__template_name
    
    def get_task_query(self):
        return self.__task_query

    def get_model_compatibility(self):
        return self.__model_compatibility
        