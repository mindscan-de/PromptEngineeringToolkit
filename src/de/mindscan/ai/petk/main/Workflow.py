'''
Created on 13.07.2025

@author: JohnDoe
'''

class AIWorkflow(object):
    '''
    classdocs
    '''


    def __init__(self,  metadata, execute_instructions, execution_environment, task_nodes, edgedata, ai_task_descriptor):
        '''
        Constructor
        '''
        self.__metadata = metadata
        self.__execute_instructions = execute_instructions
        self.__execution_environment = execution_environment
        self.__task_nodes = task_nodes
        self.__edgedata = edgedata
        self.__ai_task_descriptor = ai_task_descriptor
    
    def getTaskNames(self):
        return [task['taskname'] for task in self.__task_nodes]
    
    def getTaskNodes(self):
        return self.__task_nodes
    
    def getWorkflowVersion(self):
        return self.__metadata['version']
    
    def getWorkflowShortDescription(self):
        return self.__metadata['short_description']
    
    def getWorkflowDescription(self):
        return self.__metadata['__description']
    
    def getInputFields(self):
        return self.__execute_instructions["inputfields"]
    
    def getWorkflowKey(self):
        return self.__metadata["name"]
    
    def updateEnvironment(self,input_key:str, value):
        self.__execution_environment[input_key] = value
        
    def getExecutionEnvironment(self):
        return self.__execution_environment
    
    def getExecutionInstructions(self):
        return self.__execute_instructions
    
    def getEdgeData(self):
        return self.__edgedata