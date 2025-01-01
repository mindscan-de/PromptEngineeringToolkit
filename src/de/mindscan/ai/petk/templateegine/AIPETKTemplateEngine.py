'''
Created on 04.10.2024

@author: JohnDoe
'''

import re
import json

class AIPETKTemplateEngine(object):
    '''
    classdocs
    '''
    
    FUN_QUOTE_AS_JSON_STRING = "quoteAsJsonString"
    FUN_TO_FIRST_UPPER = "toFirstUpper"
    FUN_PRINT_JSON_STRUCTURE = "printJsonStructure"
    FUN_APPEND_AS_JSON_STRING = "appendAsJsonString"
    

    REPLACEMENT_IF_FUNCTION_UNKNOWN = 'UNKNOWN_FUNCTION'
    REPLACEMENT_IF_KEY_UNKNOWN = 'UNKNOWN_KEY'
    
    toHEX = ['0','1','2','3', #
             '4','5','6','7', #
             '8','9','A','B', #
             'C','D','E','F']
    
    selector_pattern = re.compile(r'\{{3}#([\w._:\[\]()]+)\}{3}')
    

    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    def evaluateTemplate(self, template, value_map = None):
        if not value_map:
            value_map = {}
            
        result = ''
        
        selector_matcher = self.selector_pattern.finditer(template)
        
        last_end = 0
        for match in selector_matcher:
            result += template[last_end : match.start()]
            result += self.evaluate_selector(match.groups()[0], value_map)
            last_end = match.end()
            
        result += template[last_end:]
        
        return result        
        
        pass
    
    def evaluate_selector(self, selector, value_map):
        if ':' in selector:
            function_selector = selector.split(':', 2)
            switch = {
                AIPETKTemplateEngine.FUN_QUOTE_AS_JSON_STRING: lambda: self.json_string_quote(self.get_key_from_map(function_selector[1].strip(), value_map)),
                AIPETKTemplateEngine.FUN_TO_FIRST_UPPER: lambda: self.to_first_upper(self.get_key_from_map(function_selector[1].strip(), value_map).strip()),
                AIPETKTemplateEngine.FUN_PRINT_JSON_STRUCTURE: lambda: self.print_json_structure(self.get_key_from_map(function_selector[1].strip(), value_map)),
                AIPETKTemplateEngine.FUN_APPEND_AS_JSON_STRING: lambda: self.append_as_json_string(self.get_key_from_map(function_selector[1].strip(), value_map)),
            }
            func = switch.get(function_selector[0], lambda: self.REPLACEMENT_IF_FUNCTION_UNKNOWN)
            return func()
        else:
            return self.get_key_from_map(selector, value_map)
        
    @staticmethod
    def to_first_upper(value):
        if len(value) >= 2:
            return value[0].upper() + value[1:]
        return value.upper()

    @staticmethod
    def get_key_from_map(selector, value_map):
        return value_map.get(selector, AIPETKTemplateEngine.REPLACEMENT_IF_KEY_UNKNOWN)
    
    @staticmethod
    def print_json_structure(structure):
        ## TODO: add continuation markers ? if yes, then how?
        if structure is None:
            structure = {}
        
        return "```json\n" + json.dumps(structure,indent=2) + "\n```"
    @staticmethod
    def append_as_json_string(value):
        if value is None:
            return ""
 
        value_to_append = ", "+",".join([ json.dumps(x) for x in value ])
        
        return value_to_append

    @staticmethod
    def json_string_quote(value_to_escape):
        if not value_to_escape:
            return None
        
        builder = []
        
        for c in value_to_escape:
            if c == '\\' or c == '"':
                builder.extend(['\\', c])
            elif ord(c) >= 0 and ord(c) <= 0x1f:
                builder.append('\\')
                if c == '\n':
                    builder.append('n')
                elif c == '\r':
                    builder.append('r')
                elif c == '\t':
                    builder.append('t')
                elif c == '\f':
                    builder.append('f')
                elif c == '\b':
                    builder.append('b')
                else:
                    builder.extend(["u00", 
                                    AIPETKTemplateEngine.toHEX[(ord(c) >> 4) & 0x1],
                                    AIPETKTemplateEngine.toHEX[(ord(c)) & 0xF]])
            elif ord(c) >= 0xD800 and ord(c) <= 0xDFFF:
                builder.extend(["\\u",
                                AIPETKTemplateEngine.toHEX[(ord(c) >> 12) & 0xf],
                                AIPETKTemplateEngine.toHEX[(ord(c) >> 8) & 0xf],
                                AIPETKTemplateEngine.toHEX[(ord(c) >> 4) & 0xf],
                                AIPETKTemplateEngine.toHEX[(ord(c)) & 0xf]])
            else:
                builder.append(c)
                
        return "\"" + ''.join(builder) + "\""
            
