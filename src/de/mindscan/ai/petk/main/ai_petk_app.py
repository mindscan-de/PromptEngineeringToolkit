'''
Created on 22.09.2024

MIT License

Copyright (c) 2024 Maxim Gansert

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
import os
import json

from de.mindscan.ai.petk.llmaccess.lm_apitypes import get_RemoteApiTypes
from de.mindscan.ai.petk.llmaccess.lm_connection_endpoints import getConnectionEndpoints
from de.mindscan.ai.petk.llmaccess.APIType import ANSWER_KEY_CONTENT
from de.mindscan.ai.petk.llmaccess.transport.RemoteApiModelInvoker import RemoteApiModelInvoker
from de.mindscan.ai.petk.llmaccess.lm_modeltypes import get_ModelTypes
from de.mindscan.ai.petk.taskaccess.aitask.ai_tasktemplates import get_ai_task_tasktemplates
from de.mindscan.ai.petk.templateegine.AIPETKTemplateEngine import AIPETKTemplateEngine
from de.mindscan.ai.petk.main.wf_executor import prepareWorkflow, executeWorkflow2

# Set the wide mode and application name
st.set_page_config(layout="wide", page_title="Prompt-Engineering-Toolkit")
st.markdown("""<style>textarea { font-family:Courier New important!; } </style>""", unsafe_allow_html=True)
# WE do want to initialize the UI if session is not properly initialized 

ai_task_directory = "../../../../../../ai_tasks"
endpointname = "bigserverOobaboogaEndpoint"

## ----------------------------
## Prompt Engineering Tabs
## ----------------------------

def render_ai_templates_tab(tab):
    with tab:
        ai_task_templates = get_ai_task_tasktemplates()
        task_name_container, ai_task_container = st.columns([0.25,0.75])
        
        with task_name_container:
            settings_aitemplates_selected_aitasktemplate = st.selectbox("Select AI Task-Template", ai_task_templates.keys(),key="llm_pe.aitemplates.selected.aitasktemplate")
            pass
        with ai_task_container:
            # we want to figure out, what the template configurations are
            aitasktemplate = ai_task_templates[settings_aitemplates_selected_aitasktemplate]
            
            st.text_area("System-Prompt", value=aitasktemplate.get_systemm_prompt(), height=160, key="llm_pe.aitemplates.selected.systemprompt")
            st.text_area("Task Query", value=aitasktemplate.get_task_query(), key="llm_pe.aitemplates.selected.taskquery")
            st.text_area("Task-Context Template", value=aitasktemplate.get_task_context_template(), key="llm_pe.aitemplate.selected.taskcontexttemplate")
            st.text_area("Task-Answer Pretext Template", value=aitasktemplate.get_task_answer_pretext_template(), key="llm_pe.aitemplate.selected.taskanswerpretexttemplate")
            
            st.write("#### Task To Model Compatibility")
            st.text_input("Model Compatibility", value=aitasktemplate.get_model_compatibility(), disabled=True, key="llm_pe.aitemplate.selected.taskmodelcompatibility")
            pass
        
        
        ideas ={
                'unittest': ['generate java4 unit test from code/complete the unit tests'],
                'refactor': [
                    'simplify_code',
                    'improve_variable_names',
                    'split_method',
                    'performance_optimize_code'
                    ],
                'reengineer': [
                    ],
                # output as json
                'architect': [
                    'TODO SYSTEMPROMPT',
                    'collect, suggest and list technologies read from specification', 
                    'do a systemprompt for architecture',
                    'select an architectural template from a list of templates ',
                    'configure a project'
                    ],
                'bug-hunter': [
                    'TODO SYSTEMPROMPT',
                    'bug_found_or_add_logs',
                    'get_bug_reproduction_instructions',
                    'iteration',
                    'log_data',
                    ],
                'coder': [
                    'TODO SYSTEMPROMPT',
                    'breakdown',
                    'describe_file',
                    'implement_changes',
                    'iteration',
                    '(apply_)review_feedback'
                    ],
                'code-reviewer': [
                    "TODO SYSTEMPROMPT",
                    'breakdown',
                    'review_changes',
                    ],
                'developer': [
                    "TODO SYSTEMPROMPT",
                    "breakdown",
                    "filter_files",
                    "filter files_loop"
                    "iteration",
                    "parse_task",
                    ],
                "error-handler": [
                    "debug"
                    ],
                "executor": [
                    "ran_command", # contains/parses the result of an execution provide data as json
                    ],
                "external-docs": [
                    "TODO SYSTEMPROMPT",
                    "create-doc_queries",
                    "select-docset"
                    ],
                "importer": [],
                "partials": [
                    "coding_rules",
                    "doc_snippets",
                    "execution_order",
                    "features_list",
                    "file_naming",
                    "file_size_limit",
                    "files_descriptions",
                    "files_list",
                    "files_list_relevant",
                    "filter_files_actions",
                    "human_intervention_explanation",
                    "project_details",
                    "projectr_tasks",
                    "relative_paths",
                    "user_feedback",
                    ],
                "problem-solver": [
                    "TODO SYSTEMPROMPT",
                    "get_alternative_solution",
                    "iteration"
                    ],
                "spec-writer": [
                    "TODO SYSTEMPROMPT",
                    "add_new_feature",
                    "ask_questions",
                    "prompt_complexity",
                    "review_spec"
                    ],
                "task-reviewer": [
                    "TODO SYSTEMPROMPT",
                    "review_task"
                    ],
                "tech_lead": [
                    "TODO SYSTEMPROMPT",
                    "plan",
                    "update_plan",
                    ],
                "tech-writer": [
                    "TODO SYSTEMPROMPT",
                    "create readme"
                    ],
                "trouble-shooter": [
                    "TODO SYSTEMPROMPT",
                    "breakdown",
                    "bug_report",
                    "define_user_review_goal",
                    "filter_files",
                    "filter_files_loop",
                    "get_route_files",
                    "get run_command",
                    "iteration"
                    ],
                
                "refactor": [
                    "TODO SYSTEMPROMPT",
                    "rewrite code from java to python",
                    "rewrite code from python to java"
                    ],
                
                "screenwriter/director": [
                    "TODO SYSTEMPROMPT",
                    "write story",
                    "write screenplay",
                    "write scene",
                    "describe scene in details such that it can be generated by text2img"
                    ]
            }
        
        st.write("### More Ideas")
        st.write(ideas)
        
def unJsonify(jsonString):
    if jsonString is None or jsonString == "":
        return ""
    try:
        return json.loads('"'+jsonString+'"')
    except:
        return jsonString
        
def render_ai_template_tryout_tab(tab):
    with tab:
        st.write("Hello World!")
        st.write("TODO: select template")
        st.write("TODO: identify variables in template")
        st.write("TODO: provide input fields for identified variables")
        st.write("TODO: execute model based QA task with pretext")
        st.write("TODO: select model")
        st.write("TODO: execute task")
        st.write("TODO: provide result")
        st.write("TODO: render result")
        st.write("TODO: save result for later replay (Viewer)")
        
def render_ai_agent_tasks_tab(tab):
    with tab:
        template_engine = AIPETKTemplateEngine(None)
        
        json_api_template = '''
You are a software architect. Define the required software components for {{{#project.ultraShortDescription}}} called "{{{#project.name}}}". 

Task: Provide the answer as a json structure. Output format:
{{{#printJsonStructure:output.jsonFormat}}}

Answer:
```json
        '''
        
        json_api_values = {
            'project.name': "FastBackup",
            'project.ultraShortDescription': "a Data Archiving System",
            'output.jsonFormat': { 
                "components":
                    [
                        {
                            "Component": "COMPONENTNAME",
                            "Description": "Medium length description of Component"
                        }
                    ]
                }
            }
        
        evaluated = template_engine.evaluateTemplate(json_api_template,json_api_values)
        st.code(evaluated)
        
        pass

def render_prompt_engineer_tab(tab):
    with tab:
        engneer_tab, ai_template_tryout_tab, ai_templates_tab,ai_tasks_tab, ai_agent_tasks_tab, prompts_result_viewer_tab = st.tabs(['Engineering', 'AI-Template-Tryout', 'AI-Templates', 'AI-Tasks', 'AI-Agent-Tasks','Result-Viewer'])
        
        render_ai_templates_tab(ai_templates_tab)
        render_ai_template_tryout_tab(ai_template_tryout_tab)
        render_ai_agent_tasks_tab(ai_agent_tasks_tab)
        
## ----------------------------
## Workflow and Agents Tabs
## ----------------------------
def collect_workflows():
    directory = ai_task_directory
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(".json")]

def render_ai_template_task(current_task_node):
    st.write("#### System Prompt")
    st.markdown(unJsonify( current_task_node['system_prompt']))
    
    st.write("#### Task Query")
    st.markdown(unJsonify(current_task_node['task_query']))
    
    st.write("#### Task Context Template")
    st.markdown(unJsonify(current_task_node['task_context_template']))
    
    
    st.write("#### Task Answer Pretext")
    st.markdown(unJsonify(current_task_node['task_answer_pretext']))
                
def render_readuploadedfile_task(current_task_node):
    st.markdown(
        '''
        #### Read the Content of the File
        
        Output:
        * file.name -- contains the file name of the uploaded file
        * file.content.utf8 -- the file content as a single UTF-8 formatted string
        * file.content.bytes -- the file content as an array of bytes
        ''')
    
def render_rendertemplate_task(current_task_node):
    st.write("We are rendering a template")
    # calculate which template is rendererd
    # then unjsonify it
    # then present the template
    # his should be something which the render template node should be doing
    
def render_unknowntype_task(curret_task_node):
    st.write("#### This is an unknown Task to render...")
    
render_tasktype_map = {
    'ReadUploadedFile': render_readuploadedfile_task,
    'AITaskTemplate': render_ai_template_task,
    'RenderTemplate': render_rendertemplate_task,
    'default': render_unknowntype_task
    }

def render_current_task_node(current_task_tab, current_task_node):
    with current_task_tab:
        st.write(current_task_node['short_task_header'])
        input_column, output_column = st.columns(2)
        
        with input_column:
            st.write("**In**")
            for input in current_task_node['inputs']:
                st.markdown("***" + input['source']+'*** [' +input['__datatype'] + ' ] ===> ***'+input['target']+'***')
        with output_column:
            st.write("**Out**")
            for output in current_task_node['outputs']:
                st.markdown("***" + output['source']+'*** [' +output['__datatype'] + ' ] ===> ***'+output['target']+'***')
            
        render_tasktype_map[current_task_node['type']](current_task_node)
def render_workflow_tab(tab):
    with tab:
        workflows = collect_workflows()
        workflow_selection_column, workflow_content_column = st.columns([20,80])
        
        with workflow_selection_column:
            selected_workflow = st.selectbox("Choose the workflow to inspect", workflows, )
            
        if selected_workflow is None:
            return
        
        # TODO: load the workflow and 
        workflow_file = os.path.join(ai_task_directory, selected_workflow)
        
        #metadata, execute_instructions, execution_environment, task_nodes, edgedata, ai_task_descriptor 
        workflow = prepareWorkflow(workflow_file)
        
        task_names = workflow.getTaskNames()
        
        with workflow_content_column:
            # TODO: render the overall information of the LLM Workflow
            st.write(workflow.getWorkflowShortDescription() + " -- " + workflow.getWorkflowVersion())
            st.text(workflow.getWorkflowDescription())
            
            task_tabs = st.tabs(task_names+ ['runtime'])
            task_nodes = workflow.getTaskNodes()
            for current_task_tab, current_task_node in zip(task_tabs,task_nodes):
                if current_task_node is None:
                    #render_workflowruntime_info(workflow)
                    pass
                else:
                    render_current_task_node(current_task_tab, current_task_node)
        
        pass
    
    

def render_workflow_agent_engineer_tab(tab):
    with tab:
        workflow_tab, agent_tab = st.tabs(['LLM Worflows', 'LLM Agents'])
        
        ## Cuurently i don't know too much, what can be done here, but i am convinced that the AI_Tasks mus be defined first.
        render_workflow_tab(workflow_tab)
        


    
## ----------------------------
## MultipleConfigurations and Setting-tabs
## ----------------------------

def render_api_types_tab(tab):
    with tab:
        apitypes = get_RemoteApiTypes()
        selection_container, apitype_data_container = st.columns([0.25,0.75])
        with selection_container:
            settings_apitypes_selected_apitype = st.selectbox("Select Remote-API-Type", apitypes.keys(),key="settings.apitypes.selected_api.type")
            st.write("TODO: maybe allow for a create button")
        with apitype_data_container:
            current_selected_api_type = apitypes[settings_apitypes_selected_apitype]
            current_api_name = current_selected_api_type.getApiName()
            st.text_input("API-Name", value=current_api_name, disabled=True, key="settings.apitype.["+current_api_name+"].api.name")            
            st.text_input("API-Identifier", value=current_selected_api_type.getApiIndentifier(),disabled=True, key="settings.apitype.["+current_api_name+"].api.identifier")
            st.code(body=current_selected_api_type.getJsonApiTemplate(), language="json", line_numbers=False)
            
            st.write("json path answers")
            st.write(current_selected_api_type.getJsonPathQueriesForAnswers())
            
            st.write("finish reason map")
            st.write(current_selected_api_type.getFinishReasonTranslationMap())
        
        st.write("TODO: maintain the current configuration in a kind of global Object, which can be updated and keeps the UI state in case or a reload.")
        st.write("TODO: track current selection, such that the configuration of zhis APIType can be implemented")
        
def render_model_types_tab(tab):
    with tab:
        modeltypes = get_ModelTypes()
        selection_container, modeltype_data_container = st.columns([0.25,0.75])
        with selection_container:
            setting_modeltypes_selected_modeltype = st.selectbox("Select Model(-Type)", modeltypes.keys(), key="settings.modeltype.selected_model.type")
            pass
        with modeltype_data_container:
            current_selected_model_type = modeltypes[setting_modeltypes_selected_modeltype]
            current_modeltype_name = current_selected_model_type.getModelName()
            
            st.text_input("ModelType-Name", value=current_modeltype_name, disabled=True, key="settings.modeltype.["+current_modeltype_name+"].name")
            st.text_input("ModelType-Identifier", value=current_selected_model_type.getModelIdentifier(),disabled=True, key="settings.modeltype.["+current_modeltype_name+"].identifier")
            
            st.write("TODO: Raw Model Invocation Template")
            st.write("TODO: QA w pretext Template")
            st.write("TODO: QA w/o pretext Template")
            st.write("TODO: Code Completion Template")
            
            st.write("TODO: Chat templates?")
            pass
        pass        

def render_settings_tab(tab):
    with tab:
        api_types_tab, model_tab, endpoints_tab, llm_tasks_tab, general_tab = st.tabs(["API-Types", "Models", "Endpoints", "LLM-Tasks", "Misc"])
        
        render_api_types_tab(api_types_tab)
        render_model_types_tab(model_tab)
        # render endpoints_tab
        # render llm tasks (code completion, QA, QA with pretext) 
        # render general_tab
        
def render_simple_invoker_test_tab(tab):
    with tab:
        st.write("### Query")
        llm_query_input = st.text_area("LLM Query Input", height=80, key="invoker_test_tab.llm.query.input")
        
        if(llm_query_input):
            invoker = RemoteApiModelInvoker(None)
            
            endpoint = getConnectionEndpoints()[endpointname]
            structure = invoker.invoke_backend(endpoint, llm_query_input)
        
            st.write("### Answer")
        
            markdown_render_tab, json_render_tab, raw_render_tab =st.tabs(['Markdown', 'Json', 'Raw'])
            with markdown_render_tab:
                st.write(structure[ANSWER_KEY_CONTENT])
            with raw_render_tab:
                st.code(structure[ANSWER_KEY_CONTENT])
            with json_render_tab:
                st.write("```json\n"+str(structure[ANSWER_KEY_CONTENT]))
            
        pass
    
def buildModelTask(aiTaskTemplate, model_template, taskRuntimeEnvironment):
    system_prompt = aiTaskTemplate.get_systemm_prompt()
    query = aiTaskTemplate.get_task_query()
    context_template = aiTaskTemplate.get_task_context_template()
    pretext_template = aiTaskTemplate.get_task_answer_pretext_template()
    extra_stopwords = aiTaskTemplate.get_extra_stopwords()
    
    # now we must fill the contest_template and make it a context
    # now ew must fill the pretext_template and make it a pretext
    # use the template engine
    template_engine = AIPETKTemplateEngine(None)
    context = template_engine.evaluateTemplate(context_template, taskRuntimeEnvironment)
    pretext = template_engine.evaluateTemplate(pretext_template, taskRuntimeEnvironment)
    
    # now fill the model template
    task_data = {
        'system.prompt':system_prompt,
        'query':query,
        'context':context,
        'pretext':pretext,
        } 

    model_task = template_engine.evaluateTemplate(model_template, task_data)
    
    return model_task, extra_stopwords






def render_ai_task_graph_tab(tab):
    with tab:
        workflow_file = os.path.join(ai_task_directory, "StableDiffusionTiPersonDataPruning2.json")
        
        #metadata, execute_instructions, execution_environment, task_nodes, edgedata, ai_task_descriptor 
        workflow = prepareWorkflow(workflow_file)
    
        # Render the short task description
        st.write(workflow.getWorkflowShortDescription())
        
        # render the input fields
        input_fields = workflow.getInputFields()
        for input_key in input_fields.keys():
            key = workflow.getWorkflowKey()+input_key
            
            if input_fields[input_key]["__uitype"]=="textfield":
                if_value = st.text_input(input_fields[input_key]["label"], disabled=False, key = key)
                workflow.updateEnvironment(input_key, if_value)
            elif input_fields[input_key]["__uitype"]=="selectone":
                select_value = st.selectbox(input_fields[input_key]["label"], input_fields[input_key]["options"], key = key)
                workflow.updateEnvironment(input_key, select_value)
            elif input_fields[input_key]["__uitype"]=="singlefileupload":
                inputfile_value = st.file_uploader(input_fields[input_key]["label"], accept_multiple_files=False,key=input_key)
                workflow.updateEnvironment(input_key, inputfile_value)
    
        # render the execute button    
        runme = st.button("Execute",key=workflow.getWorkflowKey()+".execute")
        if(runme):
            logcontainer = st.container()
            executeWorkflow2(workflow, logcontainer)
    
        #st.write(ai_task_descriptor)
        pass
    pass
    
def render_translator_test_tab(tab):
    with tab:
        workflow_file = os.path.join(ai_task_directory,"EnglishToJapaneseTranslator.json")
        
        workflow = prepareWorkflow(workflow_file)
        
        # Render the short task description
        st.write(workflow.getWorkflowShortDescription())
        
        # render the input fields
        input_fields = workflow.getInputFields()
        for input_key in input_fields.keys():
            key = workflow.getWorkflowKey()+input_key
            value = st.text_input(input_fields[input_key]["label"], disabled=False, key = key)
            workflow.updateEnvironment(input_key, value) 
    
        
    
        # render the execute button    
        runme = st.button("Execute")
        if(runme):
            logcontainer = st.container()
            executeWorkflow2(workflow,logcontainer)
    
        #st.write(ai_task_descriptor)
        
        pass
        
        
## ----------------------------
## Main UI
## ---------------------------- 

prompt_enginener_tab, workflow_agent_engineer_tab, settings_tab, simple_invoker_tester_tab, aitask_graph_tab,translator_test_tab = st.tabs(['LLM Prompt Engineer','LLM Workflow & Agent Engineer','Settings','Simple Invocation Tests','AITask-Graph','Translator Test'])

render_prompt_engineer_tab(prompt_enginener_tab)
render_workflow_agent_engineer_tab(workflow_agent_engineer_tab)
render_settings_tab(settings_tab)
render_simple_invoker_test_tab(simple_invoker_tester_tab)
render_ai_task_graph_tab(aitask_graph_tab)
render_translator_test_tab(translator_test_tab)
