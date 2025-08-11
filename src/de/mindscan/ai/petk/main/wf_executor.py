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

def aivm_execute_instruction_rendertemplate(execution_environment, current_node):
    template = ""
    inputs = current_node["inputs"]
    for inputconnector in inputs:
        if inputconnector["target"] == "template":
            template = execution_environment[inputconnector["source"]]
        
    template_engine = AIPETKTemplateEngine(None)
    rendered = template_engine.evaluateTemplate(template, execution_environment)
    
    outputs = current_node["outputs"]
    for connector in outputs:
        if connector["source"] == "rendered":
            execution_environment[connector["target"]] = rendered

    return execution_environment


def aivm_execute_instruction_readuploadedfile(execution_environment, current_node, outputs, connector, value):
    inputfile = None
    inputs = current_node["inputs"]
    for inputconnector in inputs:
        if inputconnector["target"] == "file":
            inputfile = execution_environment[inputconnector["source"]]
    
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

def aivm_execute_instruction_boolean(execution_environment, current_node):
    # from for conversion
    fromValue = None
    inputs = current_node["inputs"]
    for inputconnector in inputs:
        if inputconnector["target"] == "fromValue":
            fromValue = execution_environment[inputconnector["source"]]
    
    outputs = current_node["outputs"]
    # TODO: toString....
    for connector in outputs:
        if connector["source"] == "true":
            value = True
        elif connector["source"] == "false":
            value = False
        elif connector["source"] == "asBoolean":
            # TODO check that fromValue is not None
            value = ( fromValue == "true" )
        elif connector["source"] == "not":
            # TODO check that fromValue is not None
            value = not( fromValue == "true" )
        else:
            value = False
            
        execution_environment[connector["target"]] = value
    
    return execution_environment


def aivm_execute_instruction_if(execution_environment, current_node, workflow, current_instruction_pointer):
    condition = False
    inputs = current_node["inputs"]
    for inputconnector in inputs:
        if inputconnector["target"] == "condition":
            condition = execution_environment[inputconnector["source"]]
    
    if condition:
        return workflow.getNextNodeName(current_instruction_pointer, "then")

    return workflow.getNextNodeName(current_instruction_pointer, "else")

def aivm_execute_instruction_nop(execution_environment, current_node):
    return execution_environment


def aivm_execute_instruction_assert_fail(execution_environment, current_node):
    st.write("## RESULT: FAIL")
    return execution_environment


def aivm_execute_instruction_assert_success(execution_environment, current_node):
    st.write("## RESULT: SUCCESS")
    return execution_environment

def aivm_execute_instruction_qa_template(execution_environment, current_node, endpoint, model_task, extra_stopwords):
    st.write(current_node["short_task_header"])
    st.write("Query")
    st.code(model_task,language="markdown")
    
    invoker = RemoteApiModelInvoker(None)    
    # now execute the model task for a given endpoint and retrieve the answer
    llm_result = invoker.invoke_backend(endpoint, model_task, {
            "extra_stopwords":extra_stopwords})
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
    
    return execution_environment


def aivm_execute_instruction_array_foreach(execution_environment, current_node, workflow,current_instruction_pointer):
    # TODO we have to process the input, such that we know the array we want to loop over and the variable name to fill...
    # then we need to determine, whether we can loop over it
    # if yes we call someone, who can help us with executing the sub graph
    body_nodes = workflow.getNextNodeName(current_instruction_pointer, "body")
    
    return execution_environment


def executeWorkflow(workflow, log_container):
    # TODO: 
    execution_environment = workflow.getExecutionEnvironment()
    
    with log_container:
        st.write("### Workflow Log Container")
        st.write("should have run it")
        st.write(execution_environment)
        ## now execute the graph....
        
        endpoint = getConnectionEndpoints()['bigserverOobaboogaEndpoint']
        
        # 1st step, first shot translation to japanese
        # let's assume we have this phing codelama model
        model = PhindCodeLama34Bv2(None)
        model_template = model.get_unstructured_prompt_template_with_context_and_pretext()
        
        ## TODO iterate, while the state exists, of the current name is not None
        current_instruction_pointer = workflow.getStartInstructionPointer()
        
        while current_instruction_pointer is not None:
            model_task, extra_stopwords, current_node = buildModelTaskFromJson(current_instruction_pointer, workflow,  model_template, execution_environment)
            
            # 
            workflow_node = workflow.getWorkflowNode(current_instruction_pointer)
            # instead of the next code, we only need to execute the workflow_node, some of them are statefule, and some aren't
            # workflow_executor.execute(worflow_node, execution_environment)
            
            
            # there are conditional nodes, which will change the outcome, where to continue next
            # there should be a for / foreach nodes, which should handle 
            # call/return
            # goto / contunie / break
            # a for wil be a separate call stack for more simplicity in the call stack.
            
            
            current_op_code = workflow_node.getOpCode()
            st.write("current Node Type : "+current_op_code ) 


            # -------------------------------------------------
            # AI-VM Instruction decoder for current instruction
            # -------------------------------------------------
            
            id_calculate_next_instructionpointer = True
            id_break_on_instruction = False
            id_endloop_as_break = False
            id_endloop_as_continue = False
            #id_endloop_as_void = False
            
            
            
            # -------------------------
            # Execute AI-VM-Instruction 
            # -------------------------
            
            # TODO: the next thing is that, we need to towk towards an table based execution
            # TODO: before that we need to align all calls 
            
            # ---------------
            # Flow-Primitives
            #----------------
            if current_op_code == "IF":
                id_calculate_next_instructionpointer = False
                current_instruction_pointer = aivm_execute_instruction_if(execution_environment, current_node, workflow, current_instruction_pointer)
            elif current_op_code == "ARRAY_FOREACH":
                id_calculate_next_instructionpointer = True
                execution_environment = aivm_execute_instruction_array_foreach(execution_environment, current_node, workflow, current_instruction_pointer)
            elif current_op_code == "CONTINUE":
                # CONTINUE - instruct a for-loop to continue or end
                # ** basically we must not calculate the next instruction
                # ** we must break the current loop, we must indicate, that a continue occurred, this will be determiend by the caller, how to handle this
                # ** locally we don't know what to do further, only the one who executes the foreach node, knows
                pass
            elif current_op_code == "BREAK":
                # BREAK - instruct a for loop to end the for loop
                # ** basically we must not calculate the next instruction
                # ** we must break the current loop, we must indicate, that a break occurred, this will be determined by the caller, how to handle this
                # ** locally we don't know what to do further, only the one who executes the foreach node, knows
                pass
            

            # -------------------
            # unit test primitive
            # also flow primitive
            # ------------------- 
            elif current_op_code == "ASSERT_FAIL":
                id_break_on_instruction = True
                id_calculate_next_instructionpointer = False
                execution_environment = aivm_execute_instruction_assert_fail(execution_environment, current_node)

            elif current_op_code == "ASSERT_SUCCESS":
                id_break_on_instruction = True
                id_calculate_next_instructionpointer = False
                execution_environment = aivm_execute_instruction_assert_success(execution_environment, current_node)
                
            
            # --------------------
            # Operation Primitives
            # --------------------
            # NOP
            elif current_op_code == "NOP":
                execution_environment = aivm_execute_instruction_nop(execution_environment, current_node)
            # BOOLEAN Primitive
            elif current_op_code == "BOOLEAN":
                execution_environment = aivm_execute_instruction_boolean(execution_environment, current_node)
                
            # ---
            # INVOKE_WORKFLOW - invoke other work flow
            # CALL - invoke another part of the local graph node 
            # RETURN
            # ** THE difference is in scoping the variables.
            # ---
            # ADD
            # CMP
            # SUB
            # AND 
            # OR
            # INC
            # DEC
            
            
            elif current_op_code == "AITaskTemplate":
                # TODO create the real 
                # maybe shift the building the QA node into the qs_templae execute instruction qa template
                execution_environment = aivm_execute_instruction_qa_template(execution_environment, current_node, endpoint, model_task, extra_stopwords)
            elif current_op_code == "ReadUploadedFile":
                execution_environment = aivm_execute_instruction_readuploadedfile(execution_environment, current_node)
            elif current_op_code == "RenderTemplate":
                execution_environment = aivm_execute_instruction_rendertemplate(execution_environment, current_node)
            else:
                pass
            
            st.write("updated environment")
            st.code(execution_environment, language="json")

            # ------------
            # UPDATE AI-VM
            # ------------ 
            
            # Do we need to stop?
            if id_break_on_instruction:
                break
            
            # Do we need to calculate the next instruction pointer?
            if id_calculate_next_instructionpointer:
                # DEPENDING on the decoded Instruction type, we need to encode whether to determine the next Node
                # this should be "currentnode.getNextInstructionPointer()" oder so
                current_instruction_pointer = workflow.getNextNodeName(current_instruction_pointer,"next")
        
        # Now do process the output nodes
        
        st.write("Final Value for the execution environment:")
        st.write(execution_environment,language="json")        
        
        pass

