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
        self.paragraph = paragraph # indicates whether a single sentence has been passed or not
        self.text = text
        self.explanation = lambda beg, allit: "*Due to the occurrence of the same letter (or sound) (i.e **{0}**) in adjacent or closely connected words (excluding commonly used words like 'a', \"the\", etc), **{1}** is considered to be an alliteration.*".format(beg, allit)

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
        # Function checks if consecutive or closely related words begin with the same letter
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
        # Function checks for alliterations based on the phonetics (when starting letters may be different)
        similar_sounds = ['c*k','v*w']
        f_ph = ['f*ph','ph*f']
        r_wr = ["r*wr","wr*r"]
        n_kn = ["n*kn", "kn*n"]
        n_gn = ["n*gn", "gn*n"]
        trigram_tuples = {}
        for i in range(len(processed_text)-1):
            trigram_tuples[i] = [processed_text[i][0]+'*' + processed_text[i+1][:2], processed_text[i][:2] + '*' + processed_text[i+1][0]]
        
        # print(trigram_tuples)

        for i, trigrams in trigram_tuples.items():
            for trigram in trigrams:
                if trigram[:-1] in similar_sounds or trigram[:-1:-1] in similar_sounds or trigram[1:] in similar_sounds or trigram[1::-1] in similar_sounds:
                # print()
                    starting_letter = processed_text[i][0]
                    if starting_letter not in alliterations:
                        alliterations[starting_letter] = []
                    if (i, processed_text[i]) not in alliterations[starting_letter]:
                        alliterations[starting_letter].append((i,processed_text[i]))

                        if i == len(processed_text) - 2:
                            starting_letter = processed_text[i+1][0]
                            if starting_letter not in alliterations:
                                alliterations[starting_letter] = []
                            if (i+1,processed_text[i+1]) not in alliterations[starting_letter]:
                                alliterations[starting_letter].append((i+1,processed_text[i+1]))

                if trigram in f_ph or trigram in r_wr or trigram in n_kn or trigram in n_gn:

                    if trigram in f_ph:
                        key = 'f'
                    elif trigram in r_wr:
                        key = 'r'
                    elif trigram in n_kn or trigram in n_gn:
                        key = 'n'
                    # starting_letter = processed_text[i][0]
                    if key not in alliterations:
                        alliterations[key] = []
                    if (i,processed_text[i]) not in alliterations[key]:
                        alliterations[key].append((i,processed_text[i]))

                        if i!= len(processed_text) - 1:
                            if (i+1,processed_text[i+1]) not in alliterations[key]:
                                alliterations[key].append((i+1, processed_text[i+1]))

                        if i == len(processed_text) - 2:
                            # starting_letter = processed_text[i+1][0]
                            if key not in alliterations:
                                alliterations[key] = []
                            if (i,processed_text[i+1]) not in alliterations[key]:
                                alliterations[key].append((i+1,processed_text[i+1]))
                        
                    else:
                        if i != len(processed_text)-1 and (i+1,processed_text[i+1]) not in alliterations[key]:
                            alliterations[key].append((i+1, processed_text[i+1]))

        # return alliterations

    def detect_alliteration_sentence(self, processed_text):
        # Function to detect alliterations (if any) given a sentence as input 
        alliterations = {}
        alliteration_list = []

        # print(processed_text)

        self.consecutive_word_checker(processed_text,alliterations)
        self.phonetic_checker(processed_text,alliterations)
        
        for letter, alliteration in alliterations.items():
            new_alliteration = {"alphabet_involved": letter, "indexed": alliteration}

            list_of_alliterations = list(map(lambda x: x[1],sorted(alliteration, key= lambda x: x[0])))
            joined_alliteration = '-'.join(list_of_alliterations)

            new_alliteration['joined'] = joined_alliteration
            new_alliteration["explanation"] = self.explanation(new_alliteration['alphabet_involved'], new_alliteration['joined'])
            # print("New:",new_alliteration)
            alliteration_list.append(new_alliteration)
        
        return alliteration_list

    def detect_alliterations(self):
        # Detect alliterations given a list of sentences
        processed_text_list = self.preprocess_para()
        if self.paragraph == 1:
            for i, processed_text in enumerate(processed_text_list):
                sentence_alliteration = {"sentence":self.text[i], "alliteration": self.detect_alliteration_sentence(processed_text)}
                self.alliteration_list.append(sentence_alliteration)
        
        else:
            sentence_alliteration = {"sentence":self.text, "alliteration": self.detect_alliteration_sentence(processed_text_list[0])}
            self.alliteration_list.append(sentence_alliteration)

        return self.alliteration_list

    def display_alliterations(self): 
        # To display alliteration along with an explanation
        for sent_allit in self.alliteration_list:
            print("\nSentence:", sent_allit['sentence'])
            print("**************************")
            if len(sent_allit['alliteration']) != 0:
                for allit in sent_allit['alliteration']:
                    print("Alphabet Involved:", allit['alphabet_involved'])
                    print("Alliteration:", allit['joined'])
                    print(allit['explanation'])
                    print("___________________________________")
            else:
                print("No alliterations found!")
                print("___________________________________")
            print()
    
    def execute(self):
        # Driver function
        return self.detect_alliterations()

if __name__ == "__main__":
    # text = input("Enter your sentence: ")
    text = ["Ninjas gnashed their knives and nailed their targets.","She wrapped the rose neatly","Dana deserved to dance with the kind king.","She rarely reads; she’d rather write her own books.","The red roses were wrapped in ribbons."]
    # text = "the cruel king was kind in real life"
    
    allit_obj = Alliteration(text, 1)
    alliterations = allit_obj.detect_alliterations()
    allit_obj.display_alliterations()
