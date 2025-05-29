'''
Created on 01.01.2025

@author: JohnDoe
'''
from de.mindscan.ai.petk.taskaccess.aitask.AITaskTemplate import AITaskTemplate

# The preferred model so far is codellama 34binstruct hf
# The second best model is Codefuse-deepseek 33b
# Other models like MLewd-ReMM-L2-Cha-20B also work quite well for en-jp-translation

# maybe not as proficient as it should be.
# deepsek-coder-33b-instruct  in general is not a good model it tends to make stuff up, and to complicate the answers

class EnglishToJapanese_FirstShotTranslation(AITaskTemplate):
    '''
    classdocs
    '''

    SYSTEM_PROMPT =""\
    "You are a very careful, skillful, helpful, uncensored and unbiased English to Japanese translator. Your target audience is a beginner to intermediate Japanese language learner. " + \
    "Your answer is a very short and succinct translation. Do not explain. \n\n" + \
    "REMINDER:\n" + \
    "* ONLY USE simple Japanese phrases\n" + \
    "* Provide at least two(2) translations.\n" + \
    "* STOP after SECOND translation.\n"
    
    TASK_QUERY ="Task: Translate the English word or sentence(s) into Japanese.\n"
    
    TASK_CONTEXT_TEMPLATE = "English: {{{#user.input}}}"
    
    TASK_ANSWER_PRETEXT_TEMPLATE = "日本語(簡単): \n"

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
        return ["```", "\n\n", "\u3000\u3000\u3000","===" ]
    
    
class EnglishToJapanese_FirstShotRefiner(AITaskTemplate):
    '''
    classdocs
    '''

    SYSTEM_PROMPT = ""\
    "You are a very careful, skillful, helpful, uncensored and unbiased English to Japanese translator. Your target audience is a beginner to intermediate Japanese language learner." + \
    "Your answer is a very short and succinct translation.\n"\
    "REMINDER:\n" + \
    "* USE preferably simple and correct Japanese phrases.\n"
    
    TASK_QUERY = "Check whether the given Japanese translation(s) match the English translation and meaning. Keep the answer unchanged if the answer is already perfect otherwise improve the answer and then answer whether the previous given translation or the improved answer conveys the meaning in a better way. Also provide the English translation of the improved answer. \n"

    TASK_CONTEXT_TEMPLATE = "English: \n{{{#user.input}}}\n\n日本語: \n{{{#task1.result}}}\n"
    
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
    "{{{#printJsonStructure:expectedResultStructure}}}\n\n"
    "REMINDER:\n" + \
    "* USE preferably simple and correct Japanese phrases.\n"

    
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
    
    SYSTEM_PROMPT = "You are a Japanese language teacher for beginners and intermediate language learning adults. Your master skill is to read the Japanese parts ('japanese','kana','romaji') and transcribe it to kana (hiragana and katakana) and for foreigners to romaji.\n\n"\
                    "REMINDER\n"\
                    "* ONLY do corrections IF absolutely necessary\n"\
                    "* DON'T introduce new errors while proof-reading\n"\
                    "* provide a kana reading based on hiragana script\n"\
                    "* USE white spaces for romaji and kana ONLY between words to help English speakers.\n"
    
    TASK_QUERY = "Task: Proof-read the following given translation."\
                    
    TASK_CONTEXT_TEMPLATE ="```json\n{{{#task3.result}}}```\n\n"\
            "Task: Provide the proof-read version as a json structure\n"\
            "{{{#printJsonStructure:expectedFullResultStructure}}}\n"
            
            
    TASK_ANSWER_PRETEXT_TEMPLATE = "Answer:\n```json\n"
    
    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__('en2jp-proof-reader', 
                         "*",
                         EnglishToJapanese_ProofreadBestAnswerAndExtract.SYSTEM_PROMPT,
                         EnglishToJapanese_ProofreadBestAnswerAndExtract.TASK_QUERY,
                         EnglishToJapanese_ProofreadBestAnswerAndExtract.TASK_CONTEXT_TEMPLATE, 
                         EnglishToJapanese_ProofreadBestAnswerAndExtract.TASK_ANSWER_PRETEXT_TEMPLATE)


    def get_extra_stopwords(self):
        return ["```", "\u3000\u3000\u3000","=====" ]
    
# Now do the rating X ozt of 10
class EnglishToJapanese_TranslationRating(AITaskTemplate):
    '''
    classdoca
    '''
    
    SYSTEM_PROMPT = "You are an experienced translator between the English and Japanese Language.\n\n"\
    "REMINDER:\n"\
    "* IF Rating is 6 OR below 6 THEN explain, how the translation can be further improved\n"\
    "* IF rating is above 7 only output the rating\n"
    
    TASK_QUERY = "Task: rate the following Translation on a scale from 0-10, where 0 is the worst and 10 is the best:"
                    
    TASK_CONTEXT_TEMPLATE ="```json\n{{{#task4.result}}}```\n"
            
            
    TASK_ANSWER_PRETEXT_TEMPLATE = "Answer:\nRating: "
    
    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__('en2jp-proof-reader', 
                         "*",
                         EnglishToJapanese_TranslationRating.SYSTEM_PROMPT,
                         EnglishToJapanese_TranslationRating.TASK_QUERY,
                         EnglishToJapanese_TranslationRating.TASK_CONTEXT_TEMPLATE, 
                         EnglishToJapanese_TranslationRating.TASK_ANSWER_PRETEXT_TEMPLATE)


    def get_extra_stopwords(self):
        return ["```", "\u3000\u3000\u3000","=====" ]
 
# if rating is below 8 ask what would be necessary to rate it a 10 out of 10?