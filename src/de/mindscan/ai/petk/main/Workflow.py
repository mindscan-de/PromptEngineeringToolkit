'''
Created on 13.07.2025

@author: JohnDoe
'''

import json

AI_TASK_DESCRIPTOR_KEY_EXECUTE_INSTRUCTIONS = "execute"
AI_TASK_DESCRIPTOR_KEY_NODEDATA = "nodedata"
AI_TASK_DESCRIPTOR_KEY_METADATA = "__metadata"
AI_TASK_DESCRIPTOR_KEY_EDGEDATA = "edgedata"
AI_TASK_DESCRIPTOR_KEY_DATADICTIONARY = "json_data_dictionary"


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
    
    def getEntryNodeName(self):
        return self.getExecutionInstructions()['entry']
    
    def getNextNodeName(self, current_node_name, trasition_name="next"):
        ## TODO
        ## if there s only one next node, aczally we need to ask the task node whch is the next node, instead of
        ## asking the workflow for the next node.
        if current_node_name in self.__edgedata["connections"]:
            return self.__edgedata["connections"][current_node_name][trasition_name][0] or None
        return None

    
def workflowFromJsonFile(workflow_file):
    execute_instructions = {}
    task_nodes = []
    execution_environment = {}
    with open(workflow_file, 'r', encoding='utf-8') as json_file:
        ai_task_descriptor = json.load(json_file)
        execute_instructions = ai_task_descriptor[AI_TASK_DESCRIPTOR_KEY_EXECUTE_INSTRUCTIONS]
        task_nodes = ai_task_descriptor[AI_TASK_DESCRIPTOR_KEY_NODEDATA]['nodes']
        metadata = ai_task_descriptor[AI_TASK_DESCRIPTOR_KEY_METADATA]
        edgedata = ai_task_descriptor[AI_TASK_DESCRIPTOR_KEY_EDGEDATA]
        jsondata_dictionary = ai_task_descriptor[AI_TASK_DESCRIPTOR_KEY_DATADICTIONARY]
    # basicalls this should be part of a process not part of the workflow, the workflow is basically the template of the process, 
    # the runtime.environment data should be part of an AI process
    for json_key in jsondata_dictionary.keys():
        structure = jsondata_dictionary[json_key]
        execution_environment[json_key] = structure
    
    return AIWorkflow(metadata, execute_instructions, execution_environment, task_nodes, edgedata, ai_task_descriptor)

