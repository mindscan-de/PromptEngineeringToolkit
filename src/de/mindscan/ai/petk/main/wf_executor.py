'''
Created on 29.06.2025

MIT License

Copyright (c) 2025 Maxim Gansert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@author: Maxim Gansert

'''
import streamlit as st
from de.mindscan.ai.petk.llmaccess.transport.RemoteApiModelInvoker import RemoteApiModelInvoker
from de.mindscan.ai.petk.llmaccess.lm_connection_endpoints import getConnectionEndpoints

from de.mindscan.ai.petk.llmaccess.translate.modeltypes.PhindCodeLama34Bv2 import PhindCodeLama34Bv2
from de.mindscan.ai.petk.templateegine.AIPETKTemplateEngine import AIPETKTemplateEngine
from de.mindscan.ai.petk.main.Workflow import workflowFromJsonFile


def prepareWorkflow(workflow_file):
    return workflowFromJsonFile(workflow_file)



def buildModelTaskFromJson(current_node_name, workflow, model_template, taskRuntimeEnvironment):
    task_nodes = workflow.getTaskNodes()
    
    current_node = None
    for task_node in task_nodes:
        if task_node["taskname"] == current_node_name:
            current_node = task_node
    
    if current_node is None:
        return "",[]
    
    if current_node["type"] != "AITaskTemplate":
        return "",[],current_node
        
    
    system_prompt = current_node["system_prompt"]
    query = current_node["task_query"]
    context_template = current_node["task_context_template"]
    pretext_template = current_node["task_answer_pretext"]
    extra_stopwords = current_node["extra_stopwords"] or []
    
    template_engine = AIPETKTemplateEngine(None)
    context = template_engine.evaluateTemplate(context_template, taskRuntimeEnvironment)
    pretext = template_engine.evaluateTemplate(pretext_template, taskRuntimeEnvironment)
    
    task_data = {
        'system.prompt':system_prompt,
        'query':query,
        'context':context,
        'pretext':pretext,
        } 

    model_task = template_engine.evaluateTemplate(model_template, task_data)

    return model_task, extra_stopwords, current_node


# Basic workflow execution extraction

def executeRenderTemplateNode(execution_environment, current_node):
    template = ""
    inputs = current_node["inputs"]
    for inputconnector in inputs:
        if inputconnector["target"] == "template":
            template = execution_environment[inputconnector["source"]]
            break
        
    template_engine = AIPETKTemplateEngine(None)
    rendered = template_engine.evaluateTemplate(template, execution_environment)
    
    outputs = current_node["outputs"]
    for connector in outputs:
        if connector["source"] == "rendered":
            execution_environment[connector["target"]] = rendered

    return execution_environment


def executeReadUploadedFileNode(execution_environment, current_node, outputs, connector, value):
    inputfile = None
    inputs = current_node["inputs"]
    for inputconnector in inputs:
        if inputconnector["target"] == "file":
            inputfile = execution_environment[inputconnector["source"]]
            break
    
    if inputfile is not None:
        outputs = current_node["outputs"]
        for connector in outputs:
            value = None
            if connector["source"] == "file.name":
                value = inputfile.name
            elif connector["source"] == "file.content.utf8":
                value = inputfile.getvalue().decode("utf-8")
            elif connector["source"] == "file.content.bytes":
                value = inputfile.getValue()
            else:
                value = None
            execution_environment[connector["target"]] = value
            
    return execution_environment

def executeWorkflow(workflow, log_container):
    # TODO: 
    execution_environment = workflow.getExecutionEnvironment()
    
    with log_container:
        st.write("### Workflow Log Container")
        st.write("should have run it")
        st.write(execution_environment)
        ## now execute the graph....
        
        invoker = RemoteApiModelInvoker(None)
        endpoint = getConnectionEndpoints()['bigserverOobaboogaEndpoint']
        
        # 1st step, first shot translation to japanese
        # let's assume we have this phing codelama model
        model = PhindCodeLama34Bv2(None)
        model_template = model.get_unstructured_prompt_template_with_context_and_pretext()
        
        ## TODO iterate, while the state exists, of the current name is not None
        current_instruction_pointer = workflow.getStartInstructionPointer()
        
        while current_instruction_pointer is not None:
            model_task, extra_stopwords, current_node = buildModelTaskFromJson(current_instruction_pointer, workflow,  model_template, execution_environment)
            
            
            # workflow_node = workflow.getWorkflowNode(current_instruction_pointer)
            # instead of the next code, we only need to execute the workflow_node, some of them are statefule, and some aren't
            # workflow_executor.execute(worflow_node, execution_environment)
            
            
            # there are conditional nodes, which will change the outcome, where to continue next
            # there should be a for / foreach nodes, which should handle 
            # call/return
            # goto / contunie / break
            # a for wil be a separate call stack for more simplicity in the call stack.
            
            
            
            current_node_type = current_node["type"]
            st.write("current Node Type : "+current_node_type ) 

            # Primitives
            if current_node_type == "IF":
                condition = False
                inputs = current_node["inputs"]
                for inputconnector in inputs:
                    if inputconnector["target"] == "condition":
                        condition = execution_environment[inputconnector["source"]]
                        break
                if condition:
                    current_instruction_pointer = workflow.getNextNodeName(current_instruction_pointer,"then")
                else:
                    current_instruction_pointer = workflow.getNextNodeName(current_instruction_pointer,"else")
                #  avoid calculating the next node
                continue
            # unit test primitive 
            elif current_node_type == "ASSERT_FAIL":
                st.write("## RESULT: FAIL")
                break
            # unit test primitive
            elif current_node_type == "ASSERT_SUCCESS":
                st.write("## RESULT: SUCCESS")
                break
            
            # FOREACH
            # CONTINUE - instruct a for-loop to continue or end
            # BREAK - instruct a for loop to end the for loop
            # ---
            # INVOKE_WORKFLOW - invoke other work flow
            # CALL - invoke another part of the local graph node 
            # RETURN
            # ---
            # ADD
            # CMP
            # SUB
             
            
            elif current_node_type == "AITaskTemplate":
                # execute this
                # update the environment according to the outputs
                st.write(current_node["short_task_header"])
                st.write("Query")
                st.code(model_task,language="markdown")
                
                # now execute the model task for a given endpoint and retrieve the answer
                    
                llm_result = invoker.invoke_backend(endpoint, model_task, {
                        "extra_stopwords":extra_stopwords
                    } )
                
                ## update taskRuntimeEnvironment
                outputs = current_node["outputs"]
                for connector in outputs:
                    if connector["source"] == "local.model_task":
                        value = model_task
                    elif connector["source"] == "result.llm.response.content":
                        value = llm_result['llm.response.content']
                    else:
                        value = None
                        
                    execution_environment[connector["target"]] = value
                    
                st.write("Answer")
                st.code(llm_result['llm.response.content'])
            elif current_node_type == "ReadUploadedFile":
                execution_environment = executeReadUploadedFileNode(execution_environment, current_node)
            elif current_node_type == "RenderTemplate":
                execution_environment = executeRenderTemplateNode(execution_environment, current_node)
            else:
                pass
            
            st.write("updated environment")
            st.code(execution_environment, language="json")
            
            current_instruction_pointer = workflow.getNextNodeName(current_instruction_pointer,"next")
        
        # Now do process the output nodes
        
        st.write("Final Value for the execution environment:")
        st.write(execution_environment,language="json")        
        
        pass

