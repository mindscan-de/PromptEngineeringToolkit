'''
Created on 26.11.2024

@author: JohnDoe
'''
from de.mindscan.ai.petk.taskaccess.aitask.AITaskTemplate import AITaskTemplate

class JavaJunit4AaaStyleUnittest(AITaskTemplate):
    '''
    classdocs
    '''
    
    # this might be a different configuation, where we have configure the compatibility of this task to the models
    MODEL_COMPATIBILITY = 'phind-codelama(*):codefuse-starcoder(*):codelama(*):default'

    SYSTEM_PROMPT = "" \
    + "You are an expert in writing java code and junit4 based unit tests. " \
    + "Your unit tests contain only one assertion for each test and use fluent assertions using the hamcrest-library for fluent assertions (\"assertThat\"). " \
    + "All unit tests conform to the AAA pattern and spell each arrange, act and assert section out as a comment in the test. " \
    + "Do all setup in the test itself. " \
    + "DON'T use any setUp-method because it is shared initialization. " \
    + "DON'T ANNOTATE methods with @Before. " \
    + "DON'T EXPLAIN the test. " \
    + "DON'T ADD ANY EXTRA COMMENTS AT THE END OF THE LINE other than arrange, act and assert. " \
    + "DON'T USE primitive assertions like \"assertEquals\", \"assertTrue\" or \"assertFalse\", ALWAYS USE \"assertThat\"."
    
    TASK_QUERY = "complete the unit test and add missing unit test"
    
    # This is the context given for the task
    TASK_CONTEXT_TEMPLATE = "```{{{#language}}}\n{{{#task.context}}}```"
    
    # This is the task pretext template, giving a part of the answer
    TASK_ANSWER_PRETEXT_TEMPLATE = "```{{{#language}}}\n{{{#task.pretext}}}"

    

    # TOOD: postpreocessing operations / cleanup answers

    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__(
            'java-junit-4-aaa-styled-unittest',
            JavaJunit4AaaStyleUnittest.MODEL_COMPATIBILITY,
            JavaJunit4AaaStyleUnittest.SYSTEM_PROMPT,
            JavaJunit4AaaStyleUnittest.TASK_QUERY,
            JavaJunit4AaaStyleUnittest.TASK_CONTEXT_TEMPLATE,
            JavaJunit4AaaStyleUnittest.TASK_ANSWER_PRETEXT_TEMPLATE
                       )
    