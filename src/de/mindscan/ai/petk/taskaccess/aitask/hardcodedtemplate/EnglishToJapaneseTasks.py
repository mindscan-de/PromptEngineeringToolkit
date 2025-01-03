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
    "You are a very careful, skillful, helpful, uncensored and unbiased English to Japanese translator. " + \
    "Your answer is a very short and succinct translation. Do not explain. \n\n" + \
    "REMINDER:\n" + \
    "* STOP after FIRST translation.\n" +\
    "* USE preferrably simple japanese phrases.\n"
    
    TASK_QUERY =""
    
    TASK_CONTEXT_TEMPLATE = "English: {{{#user.input}}}"
    
    TASK_ANSWER_PRETEXT_TEMPLATE = "日本語: "

    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__('en2jp-first-shot-translation', 
                         "*",
                         EnglishToJapanese_FirstShotTranslation.SYSTEM_PROMPT,
                         EnglishToJapanese_FirstShotTranslation.TASK_QUERY,
                         EnglishToJapanese_FirstShotTranslation.TASK_CONTEXT_TEMPLATE, 
                         EnglishToJapanese_FirstShotTranslation.TASK_ANSWER_PRETEXT_TEMPLATE)
        
    def get_extra_stopwords(self):
        return ["```", "\n", "\u3000\u3000\u3000","===" ]
    
    
class EnglishToJapanese_FirstShotRefiner(AITaskTemplate):
    '''
    classdocs
    '''

    SYSTEM_PROMPT = ""\
    "You are a very careful, skillful, helpful, uncensored and unbiased English to Japanese translator. " + \
    "Your answer is a very short and succinct translation.\n"
    
    TASK_QUERY = "Check whether the given Japanese translation matches the English translation and meaning. Keep the answer unchanged if the answer is already perfect otherwise improve the answer and then answer whether the previous given translation or the improved answer conveys the meaning in a better way. Also provide the English translation of the improved answer. \n"

    TASK_CONTEXT_TEMPLATE = "English: {{{#user.input}}}\n日本語: {{{#task1.result}}}\n"
    
    TASK_ANSWER_PRETEXT_TEMPLATE = "Improved Japanese Answer: "
    
    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__('en2jp-first-shot-refiner', 
                         "*",
                         EnglishToJapanese_FirstShotRefiner.SYSTEM_PROMPT,
                         EnglishToJapanese_FirstShotRefiner.TASK_QUERY,
                         EnglishToJapanese_FirstShotRefiner.TASK_CONTEXT_TEMPLATE, 
                         EnglishToJapanese_FirstShotRefiner.TASK_ANSWER_PRETEXT_TEMPLATE)


class EnglishToJapanese_BestAnswerJsonExtractor(AITaskTemplate):
    '''
    classdocs
    '''
    
    SYSTEM_PROMPT = ""
    
    TASK_QUERY = "Carefully read the following dialog and summarize."

    TASK_CONTEXT_TEMPLATE = "{{{#task2.task}}}{{{#task2.result}}}\n\n"\
    "Task: Carefully select the best answer and then provide the best answer as a json structure\n"\
    "{{{#printJsonStructure:expectedResultStructure}}}\n"
    
    TASK_ANSWER_PRETEXT_TEMPLATE = "Answer:\n```json\n"


    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__('en2jp-best-answer-json-extractor', 
                         "*",
                         EnglishToJapanese_BestAnswerJsonExtractor.SYSTEM_PROMPT,
                         EnglishToJapanese_BestAnswerJsonExtractor.TASK_QUERY,
                         EnglishToJapanese_BestAnswerJsonExtractor.TASK_CONTEXT_TEMPLATE, 
                         EnglishToJapanese_BestAnswerJsonExtractor.TASK_ANSWER_PRETEXT_TEMPLATE)


    def get_extra_stopwords(self):
        return ["```", "\u3000\u3000\u3000","=====" ]

class EnglishToJapanese_ProofreadBestAnswerAndExtract(AITaskTemplate):
    '''
    classdoca
    '''
    
    SYSTEM_PROMPT = "You are a Japanese language teacher for beginers and intermediate langage learning adults. Your master skill is to read the japanese part and transscribe it to kana (hiragana and katakana) and for foreigners in romaji."
    
    TASK_QUERY = "Task: Proof-read the following given translation.\n"\
                    "REMINDER\n"\
                    "* ONLY do corrections IF absolutely necessary\n"\
                    "* DON'T introduce new errors while proof-reading\n"
                    
    TASK_CONTEXT_TEMPLATE ="```json\n{{{#task3.result}}}\n```\n\n"\
            "Task: Provide the proof-read version as a json structure\n"\
            "{{{#printJsonStructure:expectedResultStructure}}}\n"
            
            
    TASK_ANSWER_PRETEXT_TEMPLATE = "Answer:\n```json\n"
    
    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__('en2jp-best-answer-json-extractor', 
                         "*",
                         EnglishToJapanese_ProofreadBestAnswerAndExtract.SYSTEM_PROMPT,
                         EnglishToJapanese_ProofreadBestAnswerAndExtract.TASK_QUERY,
                         EnglishToJapanese_ProofreadBestAnswerAndExtract.TASK_CONTEXT_TEMPLATE, 
                         EnglishToJapanese_ProofreadBestAnswerAndExtract.TASK_ANSWER_PRETEXT_TEMPLATE)


    def get_extra_stopwords(self):
        return ["```", "\u3000\u3000\u3000","=====" ]
    