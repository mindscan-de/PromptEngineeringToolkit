'''
Created on 23.11.2024

@author: JohnDoe
'''
from de.mindscan.ai.petk.llmaccess.translate.ModelType import ModelType

class PhindCodeLama34Bv2(ModelType):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__("phind-codelama-34b-v2", "uuid of 'phind-codelama-34b-v2'")

    def get_qa_prompt_template_with_context(self):
        return \
            "\n" + \
            "<<SYS>> {{{#system.prompt}}} <</SYS>>\n" + \
            "Question: {{{#query}}}\n" +  \
            "Context: [begin of context] {{{#context}}} [end of context]\n" + \
            "Answer: "


    def get_qa_prompt_template_with_context_and_pretext(self):
        return \
            "\n" + \
            "<<SYS>> {{{#system.prompt}}} <</SYS>>\n" + \
            "Question: {{{#query}}}\n" + \
            "Context: [begin of context] {{{#context}}} [end of context]\n" + \
            "Answer: {{{#pretext}}}"
            
    def get_simple_code_completion_template(self):
        return "```{{{#language}}}\n{{{#context}}}"
    
    def get_raw_template(self):
        return "{{{#context}}}"
        
        