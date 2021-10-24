"""
TOKENS:
Past:   
        VBD verb, past tense took
        VBN verb, past participle taken
Present: 
        VBP verb, sing. present, non-3d take
        VBG verb, gerund/present participle taking
        VBZ verb, 3rd person sing. present takes
Future: 
        MD modal could, will
NN noun, singular 'desk'
NNS noun plural 'desks'
"""

"""
RULES:
Past:
    Past Simple: Second form of verb only (past)
    Past Continuous: was/were + verb + ing
    Past Perfect: Had + past partciple
    Past Perfect Continuous: Had been + verb + ing
Present:
    Present Simple: Verb + s/es
    Present Continuous: Is/am/are + verb + ing
    Present Perfect: Has/have + past partciple
    Present Perfect Continuous: Has/have + been + verb + ing
Future:
    Future Simple: Shall/will + verb
    Future continuous: Shall/will + be + verb + ing
    Future Perfect: Shall/will + have + past partciple
    Future Perfect Continuous: Shall/will + have + been + verb + ing
Verb Forms:
First Form: Verb
Second Form: Past 
Third Form: Past Participle
"""
import spacy
nlp = spacy.load("en_core_web_sm")
from nltk import word_tokenize, pos_tag
import nltk
from nltk.corpus import stopwords
import re
import pandas as pd 
import numpy as np 

class Tenses:
    def __init__(self, text, paragraph = 0): 
        self.tense_list = []
        self.paragraph = paragraph # indicates whether a single sentence has been passed or not
        self.text = text
        #self.explanation = lambda beg, allit: "*Due to the occurrence of the same letter (or sound) (i.e **{0}**) in adjacent or closely connected words (excluding commonly used words like 'a', \"the\", etc), **{1}** is considered to be an alliteration.*".format(beg, allit)

    def preprocess_text(self, text):
        # Removal of stopwords
        # Conversion to lowercase
        # Removal of punctuation

        words = stopwords.words("english")    
        convert = lambda x: " ".join([i for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower()
        return convert(text)

    def preprocess_para(self):
        if self.paragraph == 1:
            preprocessed_para = sentence.split('.')
            #print(preprocessed_para)
            return preprocessed_para
        else:
            return [self.text]

    def findVerbs(self, text): #takes input as single sentence, does not split at conjunction
        text_doc = nlp(text)
        #print(text_doc)
        mainClause = {} #{verb, aux, sub}
        for i in text_doc:
            if(i.dep_ == 'ROOT'):
                mainClause['verb'] = i
                mainClause['aux'] = []
                mainClause['sub'] = ''
                for j in i.children: #ccomp, advcl, only aux, no aux
                    if(j.dep_ == 'aux'):
                        mainClause['aux'].append(j)
                    elif(j.dep_ == 'nsubj'):
                        mainClause['sub'] = j.text
        return mainClause
    
    def tenseDetector(self, text):
        #print(text)
        #mainclause
        mainClause = self.findVerbs(text)
        #print(mainClause)
        mainVerb = [mainClause['verb'].text, mainClause['verb'].tag_]
        #print(mainVerb)
        auxVerbAndTag = []
        for i in mainClause['aux']:
            auxVerbAndTag.append({'aux': i.text, 'tag': i.tag_})
        #print(auxVerbAndTag)
        auxVerb = [] #only auxillary verbs
        for i in auxVerbAndTag:
            auxVerb.append(i['aux'])
        
        subject = mainClause['sub']
        modals = ['can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must', 'ought']
        tense = ""
        explanation = ""

        if auxVerb == []: #no auxilary verb sentences: she went/ she came/ she cried etc
            if(mainVerb[1] == 'VBD'):
                tense = "Past Simple"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the past tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            elif(mainVerb[1] in ['VBP', 'VBZ', 'VB', 'NN', 'NNS']):
                tense = "Present Simple"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the present tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            elif(mainVerb[1] == 'VBG'):
                tense = "Present Continuous"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the gerund/present participle form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            elif(mainVerb[1] == 'MD'):
                tense = "Future Simple"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is a modal. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        
        else:
            #future
            for i in modals:
                #print(i)
                if i in auxVerb:
                    if('be' in auxVerb and mainVerb[1] == 'VBG'):
                        tense = "Future Continuous"
                        explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'be'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                    elif(('has' in auxVerb or 'have' in auxVerb) and 'been' in auxVerb and mainVerb[1] == 'VBG'):
                        tense = "Future Perfect Continuous"
                        explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle taking and appears after 'has/have been'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                    elif(('have' in auxVerb) and mainVerb[1] == 'VBN'):
                        tense = "Future Perfect"
                        explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a past participle and appears after 'have'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                    else:
                        tense = "Future Simple"
                        explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the future tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                    return {'sentence': text, 'tense': tense, 'explanation': explanation}

            #past
            if(('was' in auxVerb or 'were' in auxVerb) and mainVerb[1] == 'VBG'):
                tense = "Past Continuous"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'was/were'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            elif('had' in auxVerb and 'been' in auxVerb and mainVerb[1] == 'VBG'):
                tense = "Past Perfect Continuous"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'had been'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            elif('had' in auxVerb and mainVerb[1] == 'VBN'):
                tense = "Past Perfect"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a past participle and appears after 'had'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            elif(mainVerb[1] == 'VBD'):
                tense = "Past Simple"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the past tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            
            #present
            elif(('is' in auxVerb or 'am' in auxVerb or 'are' in auxVerb) and mainVerb[1] == 'VBG'):
                tense = "Present Continuous"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'is/am/are'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            elif(('has' in auxVerb or 'have' in auxVerb) and 'been' in auxVerb and mainVerb[1] == 'VBG'):
                tense = "Present Perfect Continuous"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'has/have been'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            elif(('has' in auxVerb or 'have' in auxVerb) and mainVerb[1] == 'VBN'):
                tense = "Present Perfect"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a past participle and appears after 'has/have'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            elif(mainVerb[1] in ['VBP', 'VBZ', 'VB']):
                if(mainVerb[1] == 'VB'):
                    if(auxVerbAndTag[0]['tag'] == 'VBD'):
                        tense = "Past Simple"
                    else:
                        tense = "Present Simple"
                else:
                    tense = "Present Simple"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the present tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            elif(mainVerb[1] == 'VBG'):
                tense = "Present Continuous"
                explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
            
        return {'sentence': text, 'tense': tense, 'explanation': explanation}

    def detect_tense(self):
        # processed_text_list = self.preprocess_para()
        #print(processed_text_list)
        if self.paragraph == 1:
            for i in self.text:
                try:
                    #print(i)
                    result = self.tenseDetector(i)
                    #print(result)
                    sentence_tense = {"sentence": result['sentence'], "tense": result['tense'], "explanation": result['explanation']}
                    #print(sentence_tense)
                    self.tense_list.append(sentence_tense)
                    #print(self.tense_list)
                except Exception as e:
                    print("!! Text that caused error: {0}!!\n".format(i))
                    print(e)
        else:
            try: 
                result = self.tenseDetector(self.text)
                sentence_tense = {"sentence": result['sentence'], "tense": result['tense'], "explanation": result['explanation']}
                self.tense_list.append(sentence_tense)
            except Exception as e:
                    print("!! Text that caused error: {0}!!\n".format(self.text))
                    print(e)

        return self.tense_list

    def execute(self):
        # Driver function
        return self.detect_tense()

if __name__ == "__main__":
    sentence = ["I really didn’t like the movie even though the acting was good"]
    ten_obj = Tenses(sentence, 1)
    #s = sim_obj.detect_similes()
    s1=ten_obj.execute()
    print(s1)