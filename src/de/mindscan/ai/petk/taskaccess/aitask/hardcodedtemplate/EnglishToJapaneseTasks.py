'''
Created on 01.01.2025

@author: JohnDoe
'''
from de.mindscan.ai.petk.taskaccess.aitask.AITaskTemplate import AITaskTemplate

class EnglishToJapanese_FirstShotTranslation(AITaskTemplate):
    '''
    classdocs
    '''

    SYSTEM_PROMPT =""\
    "You are a very skillful English to Japanese translator. " + \
    "Your answer is a very short and succinct translation. Do not explain. \n\n" + \
    "REMINDER:\n" + \
    "* Stop after the first translation."
    
    TASK_QUERY =""
    
    TASK_CONTEXT_TEMPLATE = "English: {{{#user.input}}}"
    
    TASK_ANSWER_PRETEXT_TEMPLATE = "Japanese: "


    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__('en-2-jp-first-shot-tranlation', 
                         "*",
                         EnglishToJapanese_FirstShotTranslation.SYSTEM_PROMPT,
                         EnglishToJapanese_FirstShotTranslation.TASK_QUERY,
                         EnglishToJapanese_FirstShotTranslation.TASK_CONTEXT_TEMPLATE, 
                         EnglishToJapanese_FirstShotTranslation.TASK_ANSWER_PRETEXT_TEMPLATE)
        