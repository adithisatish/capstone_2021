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
        Clause = {'ROOT': {}, 'advcl': {}, 'ccomp': {}} #{{root: [{verb, aux, subj}], advcl: [verb, aux, subj], {ccomp: [verb, aux, subj]}}
        for i in text_doc:
            if(i.dep_ == 'ROOT'):
                Clause['ROOT']['verb'] = i
                aux = []
                sub = ""
                for j in i.children: #ccomp, advcl, only aux, no aux
                    if(j.dep_ == 'aux'):
                        aux.append(j)
                    elif(j.dep_ == 'nsubj' or j.dep_ == "nsubjpass"):
                        sub = j.text
                    if(j.dep_ == 'ccomp'):
                        Clause['ccomp']['verb'] = j
                        auxCcomp = []
                        subjCcomp = ""
                        for k in j.children:
                            if(k.dep_ == 'aux'):
                                auxCcomp.append(k)
                            elif(k.dep_ == 'nsubj'):
                                subjCcomp = k.text
                        Clause['ccomp']['sub'] = subjCcomp
                        Clause['ccomp']['aux'] = auxCcomp
                    elif(j.dep_ == 'advcl'):
                        Clause['advcl']['verb'] = j
                        auxAdvcl = []
                        subjAdvcl = ""
                        for k in j.children:
                            if(k.dep_ == 'aux'):
                                auxAdvcl.append(k)
                            elif(k.dep_ == 'nsubj'):
                                subjAdvcl = k.text
                        Clause['advcl']['sub'] = subjAdvcl
                        Clause['advcl']['aux'] = auxAdvcl
                Clause['ROOT']['aux'] = aux
                Clause['ROOT']['sub'] = sub
        return Clause
    
    def tenseDetector(self, clause):
        #print(text)
        #mainclause
        mainVerb = [clause['verb'].text, clause['verb'].tag_]
        print(mainVerb)
        auxVerbAndTag = []
        auxVerb = [] #only auxillary verbs
        for i in clause['aux']:
            auxVerbAndTag.append({'aux': i.text, 'tag': i.tag_})
            auxVerb.append(i.text)
        print(auxVerbAndTag)
        subject = clause['sub']
        modals = ['can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must', 'ought', '’ll', "'ll"]
        tense = ""
        explanation = ""

        if auxVerb == []: #no auxilary verb sentences: she went/ she came/ she cried etc
            if(mainVerb[1] in ['VBD', 'VBN']):
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
                if i in auxVerb:
                    if('be' in auxVerb and mainVerb[1] == 'VBG'):
                        tense = "Future Continuous"
                        explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'be'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                    elif(('has' in auxVerb or 'have' in auxVerb) and 'been' in auxVerb and mainVerb[1] == 'VBG'):
                        tense = "Future Perfect Continuous"
                        explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle taking and appears after 'has/have been'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                    elif(('have' in auxVerb) and mainVerb[1] in ['VBP', 'VBN']):
                        print('hi')
                        tense = "Future Perfect"
                        explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a past participle and appears after 'have'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                    else:
                        tense = "Future Simple"
                        explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the future tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                    return {'tense': tense, 'explanation': explanation}

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
            
        return {'tense': tense, 'explanation': explanation}

    def clauseTenseDetector(self, text):
        clause = self.findVerbs(text)
        if(clause['ccomp']):
            print("ccomp")
            clause1 = clause['ROOT']
            clause2 = clause['ccomp']
            result1 = self.tenseDetector(clause1)
            result2 = self.tenseDetector(clause2)
            if(result1['tense'] == result2['tense']):
                final_tense = result1['tense']
            elif(result2['tense'] == ""):
                final_tense = result1['tense']
            elif(result1['tense'] == ""):
                final_tense = result2['tense']
            else:
                final_tense = result1['tense'] + ' and ' + result2['tense']
            final_explanation = result1['explanation'] + result2['explanation']
            sentence_tense = {"sentence": text, "tense": final_tense, "explanation": final_explanation}

        elif(clause['advcl']):
            print("advcl")
            clause1 = clause['ROOT']
            print(clause1)
            clause2 = clause['advcl']
            print(clause2)
            result1 = self.tenseDetector(clause1)
            result2 = self.tenseDetector(clause2)
            if(result1['tense'] == result2['tense']):
                final_tense = result1['tense']
            elif(result2['tense'] == ""):
                final_tense = result1['tense']
            elif(result1['tense'] == ""):
                final_tense = result2['tense']
            else:
                final_tense = result1['tense'] + ' and ' + result2['tense']
            final_explanation = result1['explanation'] + "\n" + result2['explanation']
            sentence_tense = {"sentence": text, "tense": final_tense, "explanation": final_explanation}

        else:
            print("root")
            finalClause = clause['ROOT']
            result = self.tenseDetector(finalClause)
            sentence_tense = {"sentence": text, "tense": result['tense'], "explanation": result['explanation']}
            print("RESULT")
            print(sentence_tense)
            print()
            #print(self.tense_list)
        return sentence_tense

    def detect_tense(self):
        # processed_text_list = self.preprocess_para()
        #print(processed_text_list)
        if self.paragraph == 1:
            try:
                for i in self.text:
                    sentence_tense = self.clauseTenseDetector(i)
                    self.tense_list.append(sentence_tense)
            except Exception as e:
                print("!! Text that caused error: {0}!!\n".format(self.text))
                print(e)
        else:
            self.tense_list = []
            try: 
                print("single")
                sentence_tense = self.clauseTenseDetector(self.text)
                self.tense_list.append(sentence_tense)
            except Exception as e:
                print("!! Text that caused error: {0}!!\n".format(self.text))
                print(e)
        return self.tense_list

    def execute(self):
        # Driver function
        return self.detect_tense()

if __name__ == "__main__":
    sentence = ["The wounded man was being helped by some boys."]
    ten_obj = Tenses(sentence, 1)
    print(ten_obj.text)
    #s = sim_obj.detect_similes()
    s1=ten_obj.execute()
    print(s1)