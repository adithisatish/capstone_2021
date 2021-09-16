#Are you coming to school? - Are is recognised as proper Noun

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
    
    def tenseDetection(self, processed_text):
        tense = ""
        explanation = ""
        sentence = processed_text
        print(sentence)
        text = word_tokenize(sentence)
        tagged = pos_tag(text)
        #print(tagged)

        verbs = []
        for i in tagged:
            if(i[1] in ['VBN', 'VBD', 'VBP', 'VBG', 'VBZ', 'MD', 'VB']):
                verbs.append(i)
        #print(verbs)

        for i in range(len(verbs)):
            if(len(verbs) >= 2):
                #past
                if(re.search("was|were", verbs[i][0]) and verbs[i+1][1] == 'VBG'):
                    tense = "Past Continuous"
                    explanation = "The verb ***{0}*** is in the form of a gerund/present participle and appears after 'was/were'.\nRule for Past Continuous: was/were + verb + ing".format(verbs[i+1][1])
                    break
                elif(re.search("had", verbs[i][0]) and re.search("been", verbs[i+1][0]) and verbs[i+2][1] == 'VBG'):
                    tense = "Past Perfect Continuous"
                    explanation = "The verb ***{0}*** is in the form of a gerund/present participle and appears after 'had been'".format(verbs[i+2][1])
                    break
                elif(re.search("had", verbs[i][0]) and verbs[i+1][1] == 'VBN'):
                    tense = "Past Perfect"
                    explanation = "The verb ***{0}*** is in the form of a past participle and appears after 'had'".format(verbs[i+1][1])
                    break
                elif(verbs[i][1] == 'VBD'):
                    tense = "Past Simple"
                    explanation = "The verb ***{0}*** is in the past tense form".format(verbs[i][1])
                    break

                #present
                elif(re.search("is|am|are", verbs[i][0]) and verbs[i+1][1] == 'VBG'):
                    tense = "Present Continuous"
                    explanation = "The verb ***{0}*** is in the form of a gerund/present participle and appears after 'is/am/are'".format(verbs[i+1][1])
                    break
                elif(re.search("has|have", verbs[i][0]) and re.search("been", verbs[i+1][0]) and verbs[i+2][1] == 'VBG'):
                    tense = "Present Perfect Continuous"
                    explanation = "The verb ***{0}*** is in the form of a gerund/present participle and appears after 'has/have been'".format(verbs[i+2][1])
                    break
                elif(re.search("has|have", verbs[i][0]) and verbs[i+1][1] == 'VBN'):
                    tense = "Present Perfect"
                    explanation = "The verb ***{0}*** is in the form of a past participle and appears after 'has/have'".format(verbs[i+1][1])
                    break
                elif(verbs[i][1] in ['VBP', 'VBZ']):
                    tense = "Present Simple"
                    explanation = "The verb ***{0}*** is in the present tense form".format(verbs[i][1])
                    break
                elif(verbs[i][1] == 'VBG'):
                    tense = "Present Continuous"
                    explanation = "The verb ***{0}*** is in the form of a gerund/present participle".format(verbs[i][1])
                    break

                #future
                elif(verbs[i][1] == 'MD'):
                    if(re.search("be", verbs[i + 1][0]) and verbs[i+2][1] == 'VBG'):
                        tense = "Future Continuous"
                        explanation = "The verb ***{0}*** is in the form of a gerund/present participle and appears after 'be'".format(verbs[i+2][1])
                        break
                    elif(re.search("has|have", verbs[i+1][0]) and re.search("been", verbs[i+2][0]) and verbs[i+3][1] == 'VBG'):
                        tense = "Future Perfect Continuous"
                        explanation = "The verb ***{0}*** is in the form of a gerund/present participle taking and appears after 'has/have been'".format(verbs[i+3][1])
                        break
                    elif(re.search("have", verbs[i + 1][0]) and verbs[i+2][1] == 'VBN'):
                        tense = "Future Perfect"
                        explanation = "The verb ***{0}*** is in the form of a past participle and appears after 'have'".format(verbs[i+1][1])
                        break
                    else:
                        tense = "Future Simple"
                        explanation = "The verb ***{0}*** is in the future tense form".format(verbs[i][1])
                        break
            else:
                if(verbs[i][1] == 'VBD'):
                    tense = "Past Simple"
                    explanation = "The verb ***{0}*** is in the past tense form".format(verbs[i][1])
                    break
                elif(verbs[i][1] in ['VBP', 'VBZ']):
                    tense = "Present Simple"
                    explanation = "The verb ***{0}*** is in the present tense form".format(verbs[i][1])
                    break
                elif(verbs[i][1] == 'VBG'):
                    tense = "Present Continuous"
                    explanation = "The verb ***{0}*** is in the gerund/present participle form".format(verbs[i][1])
                    break
                elif(verbs[i][1] == 'MD'):
                    tense = "Future Simple"
                    explanation = "The verb ***{0}*** is a modal - could/ will".format(verbs[i][1])
                    break
        #print(tense)
        #print(explanation)
        return {'sentence': sentence, 'tense': tense, 'explanation': explanation}

    def detect_tense(self):
        processed_text_list = self.preprocess_para()
        #print(processed_text_list)
        if self.paragraph == 1:
            for i in processed_text_list:
                try:
                    #print(i)
                    result = self.tenseDetection(i)
                    sentence_tense = {"sentence": result['sentence'], "tense": result['tense'], "explanation": result['explanation']}
                    #print(sentence_tense)
                    self.tense_list.append(sentence_tense)
                    #print(self.tense_list)
                except Exception as e:
                    print("!! Text that caused error: {0}!!\n".format(i))
                    print(e)
        else:
            try: 
                sentence_tense = {"sentence": result['sentence'], "tense": result['tense'], "explanation": result['explanation']}
                self.tense_list.append(sentence_tense)
            except Exception as e:
                    print("!! Text that caused error: {0}!!\n".format(i))
                    print(e)

        return self.tense_list

    def execute(self):
        # Driver function
        return self.detect_tense()

if __name__ == "__main__":
    sentence = "Jack attended the program. He was sad."
    ten_obj = Tenses(sentence, 1)
    #s = sim_obj.detect_similes()
    s1=ten_obj.execute()
    print(s1)