from app.spo.SPODetector import get_oie_triplets, get_svo_from_triplet
from nltk import word_tokenize, pos_tag
import nltk
from nltk.corpus import stopwords
import re
import pandas as pd 
import numpy as np 

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
        text = "She returned the computer after noticing the damage."
        triplets = get_oie_triplets(text)
        for triplet in triplets:
            svo = get_svo_from_triplet(triplet)
        print(svo)

        subject = svo['Subject']
        print('subject index: ')
        sub_index = text.index(subject)
        print(sub_index)

        objectClause = svo['Object Clauses']
        obj = ''
        for i in objectClause:
            obj = obj + i
        print('object index: ')
        obj_index = text.index(obj)
        print(obj_index)

        voice = ""
        if sub_index < obj_index:
            voice = "Active"
        if obj_index < sub_index:
            voice = "Passive"
        
        return voice
    
    def detect_voice(self):
        processed_text_list = self.preprocess_para()
        #print(processed_text_list)
        if self.paragraph == 1:
            for i in processed_text_list:
                #print(i)
                sentence_voice = {"sentence": i, "voice": self.voiceSpoDetection(i)}
                self.voice_list.append(sentence_voice)
                #print(self.voice_list)
        else:
            sentence_voice = {"sentence":self.text, "voice": self.voiceSpoDetection(processed_text_list[0])}
            self.voice_list.append(sentence_voice)

        return self.voice_list

    def execute(self):
        # Driver function
        return self.detect_voice()

if __name__ == "__main__":
    sentence = "Jack attended the program"
    voice_obj = Voice_Spo(sentence)
    #s = sim_obj.detect_similes()
    s1=voice_obj.execute()
    print(s1)