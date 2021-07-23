# Alliteration Detection 

# Incorporates phonetics as well consecutive consonant words

# Import libraries

import pandas as pd 
import numpy as np 
import re
import nltk 
# nltk.data.path.append("D:/PESU/capstone_2021/venv")

# nltk.download("stopwords") # if not downloaded already

from nltk.corpus import stopwords

class Alliteration:

    def __init__(self, text, paragraph = 0): # Split the text and pass as a list if paragraph=1
        self.alliteration_list = []
        self.paragraph = paragraph # indicates single sentence has been passed
        self.text = text

    # Function to preprocess text
    def preprocess_text(self, text):
        # Removal of stopwords
        # Conversion to lowercase
        # Removal of punctuation

        words = stopwords.words("english")    
        convert = lambda x: " ".join([i for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower()
        return convert(text)

    # Function to preprocess every sentence in the paragraph
    def preprocess_para(self):
        if self.paragraph == 1:
            preprocessed_para = []
            for sentence in self.text:
                preprocessed_para.append(self.preprocess_text(sentence).split(' '))
            return preprocessed_para
        else:
            return [self.preprocess_text(self.text).split(' ')]

    # Functions to detect alliteration 

    def consecutive_word_checker(self, processed_text, alliterations):
        for i in range(len(processed_text)):
            if i==0: # first word
                if processed_text[i][0] == processed_text[i+1][0]:
                    starting_letter = processed_text[i][0]
                    if starting_letter not in alliterations:
                        alliterations[starting_letter] = []
                    if processed_text[i] not in alliterations[starting_letter]:
                        alliterations[starting_letter].append((i,processed_text[i]))

            elif i==len(processed_text) - 1: # last word
                if processed_text[i][0] == processed_text[i-1][0]:
                    starting_letter = processed_text[i][0]
                    if starting_letter not in alliterations:
                        alliterations[starting_letter] = []
                    if processed_text[i] not in alliterations[starting_letter]:
                        alliterations[starting_letter].append((i,processed_text[i]))
            
            elif processed_text[i][0] == processed_text[i-1][0] or processed_text[i][0] == processed_text[i+1][0]:
                starting_letter = processed_text[i][0]
                if starting_letter not in alliterations:
                    alliterations[starting_letter] = []
                if processed_text[i] not in alliterations[starting_letter]:
                    alliterations[starting_letter].append((i,processed_text[i]))
        
        # return alliterations

    def phonetic_checker(self, processed_text, alliterations):

        similar_sounds = ['c*k','v*w']
        f_ph = ['f*ph','ph*f']
        trigram_tuples = {}
        for i in range(len(processed_text)-1):
            trigram_tuples[i] = processed_text[i][0]+'*' + processed_text[i+1][:2]
        
        # print(trigram_tuples)

        for i, trigram in trigram_tuples.items():
            if trigram[:-1] in similar_sounds or trigram[:-1:-1] in similar_sounds or trigram in f_ph:
                # print()
                starting_letter = processed_text[i][0]
                if starting_letter not in alliterations:
                    alliterations[starting_letter] = []
                if processed_text[i] not in alliterations[starting_letter]:
                    alliterations[starting_letter].append((i,processed_text[i]))

                    if i == len(processed_text) - 2:
                        starting_letter = processed_text[i+1][0]
                        if starting_letter not in alliterations:
                            alliterations[starting_letter] = []
                        if processed_text[i+1] not in alliterations[starting_letter]:
                            alliterations[starting_letter].append((i+1,processed_text[i+1]))

        # return alliterations

    def detect_alliteration_sentence(self, processed_text):
        # Comparing first alphabets of consecutive words to find alliterations 
        alliterations = {}
        alliteration_list = []

        self.consecutive_word_checker(processed_text,alliterations)
        self.phonetic_checker(processed_text,alliterations)
        
        for letter, alliteration in alliterations.items():
            new_alliteration = {"begins_with": letter, "indexed": alliteration}

            list_of_alliterations = list(map(lambda x: x[1],sorted(alliteration, key= lambda x: x[0])))
            joined_alliteration = '-'.join(list_of_alliterations)

            new_alliteration['joined'] = joined_alliteration
            # print("New:",new_alliteration)
            alliteration_list.append(new_alliteration)
        
        return alliteration_list

    def detect_alliterations(self):
        processed_text_list = self.preprocess_para()
        if self.paragraph == 1:
            for i, processed_text in enumerate(processed_text_list):
                sentence_alliteration = {"sentence":text[i], "alliteration": self.detect_alliteration_sentence(processed_text)}
                self.alliteration_list.append(sentence_alliteration)
        
        else:
            sentence_alliteration = {"sentence":text, "alliteration": self.detect_alliteration_sentence(processed_text_list[0])}
            self.alliteration_list.append(sentence_alliteration)

        return self.alliteration_list

if __name__ == "__main__":
    # text = input("Enter your sentence: ")
    text = ["I knew you were trouble","Dan deserved to debate with the kind king."]
    # text = "the cruel king was kind in real life"
    # print("Sentence:", text)
    # print()

    allit_obj = Alliteration(text, 1)
    alliterations = allit_obj.detect_alliterations()

    print(alliterations)

    for sent_allit in alliterations:
        print("\nSentence:", sent_allit['sentence'])
        print("**************************")
        if len(sent_allit['alliteration']) != 0:
            for allit in sent_allit['alliteration']:
                print("Begins with:", allit['begins_with'])
                print("Alliteration:", allit['joined'])
                print("___________________________________")
        else:
            print("No alliterations found!")
            print("___________________________________")
        print()
    
    # if alliteration != '':
    #     print("Words in the alliteration:", lol)
    #     print()
    # else:
    #     print("No alliterations found!")