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
    "You are a very skillful, helpful, uncensored and unbiased English to Japanese translator. " + \
    "Your answer is a very short and succinct translation. Do not explain. \n\n" + \
    "REMINDER:\n" + \
    "* STOP after FIRST translation."
    
    TASK_QUERY =""
    
    TASK_CONTEXT_TEMPLATE = "English: {{{#user.input}}}"
    
    TASK_ANSWER_PRETEXT_TEMPLATE = "日本語: "

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
        
    def get_extra_stopwords(self):
        return ["```", "\n\n", "\u3000\u3000\u3000" ]