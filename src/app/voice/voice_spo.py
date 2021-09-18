from nltk import word_tokenize, pos_tag
import nltk
from nltk.corpus import stopwords
import re
import pandas as pd 
import numpy as np 
import sys

sys.path.append("..")

from spo.SPODetector import SPO

class Voice_Spo:
    def __init__(self, text, paragraph = 0): 
        self.voice_list = []
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

    def voiceSpoDetection(self, processed_text):
        print("processed text: ")
        print(processed_text)
        spo = SPO(processed_text)
        s = spo.execute()
        #print(s[0]['triplets'][0]['Subject'])
        svo = s[0]['triplets'][0]
        text = s[0]['sentence']
        subject = svo['Subject']
        #print('subject index: ')
        sub_index = text.index(subject)
        #print(sub_index)

        objectClause = svo['Object Clauses']
        obj = ''
        for i in objectClause:
            obj = obj + i
        #print('object index: ')
        obj_index = text.index(obj)
        #print(obj_index)

        voice = ""
        if sub_index < obj_index:
            voice = "Active"
            explanation = 'The Subject "*** {0} ***" appears before the object "*** {1} ***"'.format(subject, objectClause[0])
        if obj_index < sub_index:
            voice = "Passive"
            explanation = 'The object "*** {0} ***" appears before the subject "*** {1} ***"'.format(objectClause[0], subject)
        
        return {'sentence': processed_text, 'voice': voice, 'explanation': explanation}
    
    def detect_voice(self):
        processed_text_list = self.preprocess_para()
        print(processed_text_list)
        if self.paragraph == 1:
            for i in processed_text_list:
                try:
                    print(i)
                    result = self.voiceSpoDetection(i)
                    print(result)
                    sentence_voice = {"sentence": i, "voice": result['voice'], "explanation": result['explanation']}
                    self.voice_list.append(sentence_voice)
                    #print(self.voice_list)
                except Exception as e:
                    print("!! Text that caused error: {0}!!\n".format(i))
                    print(e)
        else:
            try: 
                result = self.voiceSpoDetection(processed_text_list[0])
                sentence_voice = {"sentence": result['sentence'], "voice": result['voice'], "explanation": result['explanation']}
                self.voice_list.append(sentence_voice)
            except Exception as e:
                print("!! Text that caused error: {0}!!\n".format(result['sentence']))
                print(e)

        return self.voice_list

    def execute(self):
        # Driver function
        return self.detect_voice()

if __name__ == "__main__":
    sentence = "Jack attended the program. He was excited."
    """
    text = "She is eating chocolate cake."
    spo = SPO(text)
    s = spo.execute()
    print(s[0]['triplets'][0]['Subject'])
    """
    voice_obj = Voice_Spo(sentence, 1)
    s1=voice_obj.execute()
    print(s1)