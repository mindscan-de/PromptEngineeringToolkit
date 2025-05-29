'''
Created on 26.11.2024

@author: JohnDoe
'''
from de.mindscan.ai.petk.taskaccess.aitask.AITaskTemplate import AITaskTemplate

class JavaToPython(AITaskTemplate):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__(
            'java-to-python',
            # JavaJunit4AaaStyleUnittest.MODEL_COMPATIBILITY,
            '',
            # JavaJunit4AaaStyleUnittest.SYSTEM_PROMPT,
            '',
            # JavaJunit4AaaStyleUnittest.TASK_QUERY
            'translate the code from java to python',
            # Context Template
            '```java\n{{{#task.context}}}```',
            # Answer Pretext Template
            '```python\n' 
            )