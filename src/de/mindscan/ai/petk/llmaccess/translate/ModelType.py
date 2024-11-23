'''
Created on 23.11.2024

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

class ModelType(object):
    '''
    classdocs
    '''
    
    def __init__(self, model_name, model_identifier):
        self.__model_name = model_name
        self.__model_identifier = model_identifier
        pass
    
    
    def getModelName(self):
        return self.__model_name
    
    def getModelIdentifier(self):
        return self.__model_identifier

    def get_qa_prompt_template_with_context(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_qa_prompt_template_with_context_and_pretext(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_simple_code_completion_template(self):
        raise NotImplementedError("Subclasses should implement this!")
    
    def get_raw_template(self):
        raise NotImplementedError("Subclasses should implement this!")
