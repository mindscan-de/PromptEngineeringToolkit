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

from de.mindscan.ai.petk.llmaccess.lm_apitypes import get_RemoteApiTypes
from de.mindscan.ai.petk.llmaccess.lm_connection_endpoints import getConnectionEndpoints
from de.mindscan.ai.petk.llmaccess.ConnectionEndpoint import ConnectionEndpoint
from de.mindscan.ai.petk.templateegine.AIPETKTemplateEngine import AIPETKTemplateEngine
from de.mindscan.ai.petk.llmaccess.RemoteApiModelInvoker import RemoteApiModelInvoker
from de.mindscan.ai.petk.llmaccess.APIType import ANSWER_KEY_CONTENT

# Set the wide mode and application name
st.set_page_config(layout="wide", page_title="Prompt-Engineering-Toolkit")

# WE do want to initialize the UI if session is not properly initialized 

## ----------------------------
## Prompt Engineering Tabs
## ----------------------------

def render_ai_templates_tab(tab):
    with tab:
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
        
        st.write(ideas)

def render_prompt_engineer_tab(tab):
    with tab:
        engneer_tab, ai_templates_tab, ai_tasks_tab, prompts_result_viewer_tab = st.tabs(['Engineering', 'AI-Templates', 'AI-Tasks', 'Result-Viewer'])
        
        render_ai_templates_tab(ai_templates_tab)
        
## ----------------------------
## Workflow and Agents Tabs
## ----------------------------

def render_workflow_agent_engineer_tab(tab):
    with tab:
        workflow_tab, agent_tab = st.tabs(['LLM Worflows', 'LLM Agents'])
        
        ## Cuurently i don't know too much, what can be done here, but i am convinced that the AI_Tasks mus be defined first.
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
            
            st.write("TODO: translateFinishReason")
        
        st.write("TODO: maintain the current configuration in a kind of global Object, which can be updated and keeps the UI state in case or a reload.")
        st.write("TODO: track current selection, such that the configuration of zhis APIType can be implemented")

def render_settings_tab(tab):
    with tab:
        api_types_tab, model_tab, endpoints_tab, llm_tasks_tab, general_tab = st.tabs(["API-Types", "Models", "Endpoints", "LLM-Tasks", "Misc"])
        
        render_api_types_tab(api_types_tab)
        # render api_tyes_tab
        # render model_tab
        # render endpoints_tab
        # render llm tasks (code completion, QA, QA with pretext) 
        # render general_tab
        
def render_simple_invokder_test_tab(tab):
    with tab:
        st.write("### Query")
        llm_query_input = st.text_area("LLM Query Input", height=16, key="invoker_test_tab.llm.query.input")
        
        if(llm_query_input):
            invoker = RemoteApiModelInvoker(None)
            
            endpoint = getConnectionEndpoints()['bigserverOobaboogaEndpoint']
            structure = invoker.invoke_backend(endpoint, llm_query_input)
        
            st.write("### Rendered Answer")
            st.write(structure[ANSWER_KEY_CONTENT])
            st.write("### Raw Answer")
            st.code(structure[ANSWER_KEY_CONTENT])
            
        pass
        
## ----------------------------
## Main UI
## ---------------------------- 

prompt_enginener_tab, workflow_agent_engineer_tab, settings_tab, simple_invoker_tester_tab = st.tabs(['LLM Prompt Engineer','LLM Workflow & Agent Engineer','Settings','Simple Invocation Tests'])

render_prompt_engineer_tab(prompt_enginener_tab)
render_workflow_agent_engineer_tab(workflow_agent_engineer_tab)
render_settings_tab(settings_tab)
render_simple_invokder_test_tab(simple_invoker_tester_tab)

