'''
Created on 13.07.2025

@author: JohnDoe
'''

import json
from de.mindscan.ai.petk.templateegine import AIPETKTemplateEngine

AI_TASK_DESCRIPTOR_KEY_EXECUTE_INSTRUCTIONS = "execute"
AI_TASK_DESCRIPTOR_KEY_NODEDATA = "nodedata"
AI_TASK_DESCRIPTOR_KEY_METADATA = "__metadata"
AI_TASK_DESCRIPTOR_KEY_EDGEDATA = "edgedata"
AI_TASK_DESCRIPTOR_KEY_DATADICTIONARY = "json_data_dictionary"

class AIWorkflowNode(object):
    
    def __init__(self, task_node, next_instructions):
        self.__task_node = task_node
        self.__next_instructions = next_instructions

    def getOpCode(self):
        return self.__task_node['type']
    
    def getFollowInstructionPointer(self, branch_name="next"):
        if branch_name not in self.__next_instructions:
            return None
    
        if len(self.__next_instructions[branch_name]) == 0:
            return None
        
        return self.__next_instructions[branch_name][0] or None
    
    def getInputMappings(self):
        return self.__task_node['inputs']
    
    def getOutputMappings(self):
        return self.__task_node['outputs']
    
    def getShortTaskHeader(self):
        return self.__task_node['short_task_header'] or ""
    
    def getVersion(self):
        return self.__task_node['version'] or "0.0.0"
    
class AILLMWorkflowNode(AIWorkflowNode):
    
    def __init__(self, task_node, next_instructions):
        super.__init__(task_node, next_instructions)

    def getSystemPrompt(self):
        return self.__task_node['system_prompt']
    
    def getQuery(self):
        return self.__task_node['task_query']
    
    def getTaskContextTemplate(self):
        return self.__task_node['task_context_template']
    
    def getTaskAnswerPretextTemplate(self):
        return self.__task_node['task_answer_pretext']

    def getExtraStopwords(self):
        return self.__task_node['extra_stopwords'] or []
    
    def getContext(self, taskRuntimeEnvironment):
        template_engine = AIPETKTemplateEngine(None)
        return template_engine.evaluateTemplate(self.getTaskContextTemplate(), taskRuntimeEnvironment)

    def getPretext(self, taskRuntimeEnvironment):
        template_engine = AIPETKTemplateEngine(None)
        return template_engine.evaluateTemplate(self.getTaskAnswerPretextTemplate(), taskRuntimeEnvironment)
    
    def getModelTask(self, taskRuntimeEnvironment, model_template ):
        # basically this node should decide, which model and model type, and query type QA/QA withpretext/SimpleQuery/or agent stuff 
        # may need to be modes later? 
        task_data = {
            'system.prompt':self.getSystemPrompt(),
            'query':self.getQuery(),
            'context':self.getContext(taskRuntimeEnvironment),
            'pretext':self.getPretext(taskRuntimeEnvironment),
            } 
        
        template_engine = AIPETKTemplateEngine(None)
        return template_engine.evaluateTemplate(model_template, task_data)
        

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
    
    def getTaskNode(self, instruction_pointer):
        for task_node in self.__task_nodes:
            if task_node["taskname"] == instruction_pointer:
                return task_node
        return None
    
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
    
    def getStartInstructionPointer(self):
        return self.getExecutionInstructions()['entry']
    
    def getNextNodeName(self, instruction_pointer, trasition_name="next"):
        ## TODO
        ## if there s only one next node, aczally we need to ask the task node whch is the next node, instead of
        ## asking the workflow for the next node.
        if instruction_pointer in self.__edgedata["connections"]:
            return self.__edgedata["connections"][instruction_pointer][trasition_name][0] or None
        return None
    
    def getWorkflowNode(self, instruction_pointer) -> AIWorkflowNode:
        task_node = self.getTaskNode(instruction_pointer)
        
        if task_node is None:
            return None
        
        # st.write(instruction_pointer)
        if instruction_pointer in self.__edgedata['connections']:
            follow_nodes = self.__edgedata['connections'][instruction_pointer] or {}
        else:
            follow_nodes = {}
        
        # -----------------------------
        # TOOD: compile this task_node,
        # -----------------------------
        # compiler ... 
        # just convert this node
        workflow_node = AIWorkflowNode(task_node, follow_nodes)
        if workflow_node.getOpCode() != "AITaskTemplate":
            return workflow_node
        # recompile node type... as AILLMWorkflowNode        
        workflow_node = AILLMWorkflowNode(task_node, follow_nodes)
        
        return workflow_node

    
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

