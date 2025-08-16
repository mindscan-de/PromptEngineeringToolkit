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
from de.mindscan.ai.petk.main.Workflow import workflowFromJsonFile,\
    AIWorkflowNode, AILLMWorkflowNode


EXECUTE_RESULT_END_OF_GRAPH = 0
EXECUTE_RESULT_BREAK = 1
EXECUTE_RESULT_CONTINUE = 2
EXECUTE_RESULT_RETURN = 3
EXECUTE_RESULT_ASSERT_FAIL = 128
EXECUTE_RESULT_ASSERT_SUCCESS = 129



def prepareWorkflow(workflow_file):
    return workflowFromJsonFile(workflow_file)


# Basic workflow execution methods - should be table driven in the future

def aivm_execute_instruction_rendertemplate(execution_environment, workflow_node:AIWorkflowNode):
    template = ""
    inputs = workflow_node.getInputMappings()
    for inputconnector in inputs:
        if inputconnector["target"] == "template":
            template = execution_environment[inputconnector["source"]]
        
    template_engine = AIPETKTemplateEngine(None)
    rendered = template_engine.evaluateTemplate(template, execution_environment)
    
    outputs = workflow_node.getOutputMappings()
    for connector in outputs:
        if connector["source"] == "rendered":
            execution_environment[connector["target"]] = rendered

    return execution_environment


def aivm_execute_instruction_readuploadedfile(execution_environment, workflow_node:AIWorkflowNode):
    inputfile = None
    inputs = workflow_node.getInputMappings()
    for inputconnector in inputs:
        if inputconnector["target"] == "file":
            inputfile = execution_environment[inputconnector["source"]]
    
    if inputfile is not None:
        outputs = workflow_node.getOutputMappings()
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

def aivm_execute_instruction_boolean(execution_environment, workflow_node:AIWorkflowNode):
    # from for conversion
    fromValue = None
    inputs = workflow_node.getInputMappings()
    for inputconnector in inputs:
        if inputconnector["target"] == "fromValue":
            fromValue = execution_environment[inputconnector["source"]]
    
    outputs = workflow_node.getOutputMappings()
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


def aivm_execute_instruction_if(execution_environment, workflow_node:AIWorkflowNode):
    condition = False
    inputs = workflow_node.getInputMappings()
    for inputconnector in inputs:
        if inputconnector["target"] == "condition":
            condition = execution_environment[inputconnector["source"]]
    
    if condition:
        return workflow_node.getFollowInstructionPointer("then")

    return workflow_node.getFollowInstructionPointer("else")

def aivm_execute_instruction_nop(execution_environment, workflow_node:AIWorkflowNode):
    return execution_environment


def aivm_execute_instruction_assert_fail(execution_environment, workflow_node:AIWorkflowNode):
    st.write("## RESULT: FAIL")
    return execution_environment


def aivm_execute_instruction_assert_success(execution_environment, workflow_node:AIWorkflowNode):
    st.write("## RESULT: SUCCESS")
    return execution_environment

def aivm_execute_instruction_qa_template(execution_environment, workflow_node:AILLMWorkflowNode):
    ## TODO: well idon't like it, but anyways this must be encapsulated here.
    endpoint = getConnectionEndpoints()['bigserverOobaboogaEndpoint']
    # the mdoel and or the compatible mdoel should be calculated somewhere.
    model = PhindCodeLama34Bv2(None)
    
    # because this is a QA Template task, 
    # we must build the model_task here, not getting it injected
    # basically this should be selected because of some properties of the workflow_node
    model_template = model.get_unstructured_prompt_template_with_context_and_pretext()
    model_task = workflow_node.getModelTask(execution_environment, model_template)
    
    st.write(workflow_node.getShortTaskHeader())
    st.write("Query")
    st.code(model_task,language="markdown")
    
    invoker = RemoteApiModelInvoker(None)    
    # now execute the model task for a given endpoint and retrieve the answer
    llm_result = invoker.invoke_backend(endpoint, model_task, {
            "extra_stopwords":workflow_node.getExtraStopwords()})
    ## update taskRuntimeEnvironment
    outputs = workflow_node.getOutputMappings()
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


def aivm_execute_instruction_array_foreach(execution_environment, workflow_node:AIWorkflowNode, workflow, log_container):
    # TODO we have to process the input, such that we know the array we want to loop over and the variable name to fill...
    # then we need to determine, whether we can loop over it
    # if yes we call someone, who can help us with executing the sub graph
    body_entry_node = workflow_node.getFollowInstructionPointer("body")
    iterate_on = None
    iterate_varname = None
    
    inputs = workflow_node.getInputMappings()
    for inputconnector in inputs:
        if inputconnector["target"] == "iterateOver":
            iterate_on = execution_environment[inputconnector["source"]]
        if inputconnector["target"] == "iterateVarname":
            iterate_varname = execution_environment[inputconnector["source"]]

    if iterate_on and iterate_varname:
        for value in iterate_on:
            execution_environment[iterate_varname] = value
            
            # TODO invoke_graph(body_entry_node)
            # TODO actually the first node of ther for loop should be the assignment to the value instead of here....
            if body_entry_node is not None:
                loopresult, execution_environment, last_executed_node = executeSubGraph(workflow, execution_environment, body_entry_node, log_container)
            
                if loopresult == EXECUTE_RESULT_ASSERT_FAIL or loopresult == EXECUTE_RESULT_ASSERT_SUCCESS:
                    # TODO: handle and pass this result to the invoker
                    return (loopresult, execution_environment, last_executed_node)
                if loopresult == EXECUTE_RESULT_CONTINUE:
                    continue
                if loopresult == EXECUTE_RESULT_BREAK:
                    break
                 
            continue
     
    if body_entry_node == None:
        return (EXECUTE_RESULT_END_OF_GRAPH, execution_environment, workflow_node)
    
    
    return (EXECUTE_RESULT_END_OF_GRAPH, execution_environment, workflow_node)


# TODO introduce return codes
def executeSubGraph(workflow, execution_environment, entry_instruction_pointer, log_container):
    current_instruction_pointer = entry_instruction_pointer

    with log_container:
        while current_instruction_pointer is not None:
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
                current_instruction_pointer = aivm_execute_instruction_if(execution_environment, workflow_node)
            elif current_op_code == "ARRAY_FOREACH":
                id_calculate_next_instructionpointer = True
                result, execution_environment, latestnode = aivm_execute_instruction_array_foreach(execution_environment, workflow_node, workflow, log_container)

                # depending whether we have a ASSERT COndition, then we must stop the execution
                if result == EXECUTE_RESULT_ASSERT_FAIL or result == EXECUTE_RESULT_ASSERT_SUCCESS:
                    return (result, execution_environment, latestnode)
                
            elif current_op_code == "CONTINUE":
                id_endloop_as_continue = True
                # CONTINUE - instruct a for-loop to continue or end
                # ** basically we must not calculate the next instruction
                # ** we must break the current loop, we must indicate, that a continue occurred, this will be determiend by the caller, how to handle this
                # ** locally we don't know what to do further, only the one who executes the foreach node, knows
                pass
            elif current_op_code == "BREAK":
                id_endloop_as_break = True
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
                execution_environment = aivm_execute_instruction_assert_fail(execution_environment, workflow_node)

            elif current_op_code == "ASSERT_SUCCESS":
                id_break_on_instruction = True
                id_calculate_next_instructionpointer = False
                execution_environment = aivm_execute_instruction_assert_success(execution_environment, workflow_node)
                
            
            # --------------------
            # Operation Primitives
            # --------------------
            # NOP
            elif current_op_code == "NOP":
                execution_environment = aivm_execute_instruction_nop(execution_environment, workflow_node)
            # BOOLEAN Primitive
            elif current_op_code == "BOOLEAN":
                execution_environment = aivm_execute_instruction_boolean(execution_environment, workflow_node)
                
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
                execution_environment = aivm_execute_instruction_qa_template(execution_environment, workflow_node)
            elif current_op_code == "ReadUploadedFile":
                execution_environment = aivm_execute_instruction_readuploadedfile(execution_environment, workflow_node)
            elif current_op_code == "RenderTemplate":
                execution_environment = aivm_execute_instruction_rendertemplate(execution_environment, workflow_node)
            else:
                pass
            
            st.write("updated environment")
            st.code(execution_environment, language="json")

            # ------------
            # UPDATE AI-VM
            # ------------ 
            
            
            # We must stoplooping.
            if id_endloop_as_break or id_endloop_as_continue:
                # TODO: we should probably just return from here
                # and indicate that 
                if id_endloop_as_break:
                    return (EXECUTE_RESULT_BREAK, execution_environment, workflow_node )
                if id_endloop_as_continue:
                    return (EXECUTE_RESULT_CONTINUE, execution_environment, workflow_node )
 
            
            # Do we need to stop?
            if id_break_on_instruction:
                if current_op_code == "ASSERT_FAIL":
                    return (EXECUTE_RESULT_ASSERT_FAIL, execution_environment, workflow_node )
                if current_op_code == "ASSERT_SUCCESS":
                    return (EXECUTE_RESULT_ASSERT_SUCCESS, execution_environment, workflow_node )
                
                break
            
            # Do we need to calculate the next instruction pointer?
            if id_calculate_next_instructionpointer:
                # DEPENDING on the decoded Instruction type, we need to encode whether to determine the next Node
                # this should be "currentnode.getNextInstructionPointer()" oder so
                current_instruction_pointer = workflow_node.getFollowInstructionPointer("next")

            continue

        return (EXECUTE_RESULT_END_OF_GRAPH, execution_environment, workflow_node)

def executeWorkflow(workflow, log_container):
    # TODO: 
    execution_environment = workflow.getExecutionEnvironment()
    
    with log_container:
        st.write("### Workflow Log Container")
        st.write("should have run it")
        st.write(execution_environment)
    
    # TODO return the updated execution environment
    # TODO handle workflow codes
    result, execution_environment, last_workflow_node = executeSubGraph(workflow, execution_environment, workflow.getStartInstructionPointer(), log_container)
    
    # TODO: maybe we have to consider to update according to the workflow, such that we can invoke workflows from workflows. 
        
    with log_container:        
        st.write("Final Value for the execution environment:")
        st.write(execution_environment,language="json")        
        
    pass

