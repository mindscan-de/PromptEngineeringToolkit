'''
Created on 26.11.2024

@author: JohnDoe
'''
from de.mindscan.ai.petk.taskaccess.aitask.hardcodedtemplate.JavaJunit4AaaStyleUnittest import JavaJunit4AaaStyleUnittest
from de.mindscan.ai.petk.taskaccess.aitask.hardcodedtemplate.JavaToPython import JavaToPython

def get_ai_task_tasktemplates():
    ai_tasktemplates = {
        'java-junit-4-aaa-styled-unittest' : JavaJunit4AaaStyleUnittest(None)
        , 'java-to-python' : JavaToPython(None)
        ## , 'python-to-java' : PythonToJava(None)
        } 
    
    return ai_tasktemplates
