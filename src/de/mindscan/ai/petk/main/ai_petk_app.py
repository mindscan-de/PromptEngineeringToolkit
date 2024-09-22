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

# Set the wide mode and application name
st.set_page_config(layout="wide", page_title="Prompt-Engineering-Toolkit")

# WE do want to initialize the UI if session is not properly initialized 

## ----------------------------
## Prompt Engineering Tabs
## ----------------------------

def render_prompt_engineer_tab(tab):
    with tab:
        engneer_tab, ai_templates_tab, ai_tasks_tab, prompts_result_viewer_tab = st.tabs(['Engineering', 'AI-Templates', 'AI-Tasks', 'Result-Viewer'])
        
        
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
            settings_apitypes_selected_apitype = st.selectbox("Select Remote-API-Type", apitypes.keys(),key="settings.apitypes.selected_apitype")
            st.write("TODO: maybe allow for a create button")
        with apitype_data_container:
            st.write(settings_apitypes_selected_apitype)
            st.write(apitypes[settings_apitypes_selected_apitype])
            st.write("TODO: show json api template, ")
            st.write("TODO: show api name")
            st.write("TODO: show api identifier")
            st.write("TODO: show json path queries for answers")
            st.write("TODO: translateFinishReason")
        
        st.write("TODO: show apitype selection")
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
        
        
## ----------------------------
## Main UI
## ---------------------------- 

prompt_enginener_tab, workflow_agent_engineer_tab, settings_tab = st.tabs(['LLM Prompt Engineer','LLM Workflow & Agent Engineer','Settings'])

render_prompt_engineer_tab(prompt_enginener_tab)
render_workflow_agent_engineer_tab(workflow_agent_engineer_tab)
render_settings_tab(settings_tab)