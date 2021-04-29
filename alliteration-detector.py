# Alliteration Detection 

# Incorporates phonetics as well consecutive consonant words

# Import libraries

import pandas as pd 
import numpy as np 
import re
import nltk 

# nltk.download("stopwords") # if not downloaded already

from nltk.corpus import stopwords

# Function to preprocess text
def preprocess(text):
    # Removal of stopwords
    # Conversion to lowercase
    # Removal of punctuation

    words = stopwords.words("english")    
    convert = lambda x: " ".join([i for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower()
    return convert(text)

# Functions to detect alliteration 

def consecutive_word_checker(processed_text, alliterations):
    for i in range(len(processed_text)):
        if i==0: # first word
            if processed_text[i][0] == processed_text[i+1][0]:
                if processed_text[i] not in alliterations:
                    alliterations.append((i,processed_text[i]))

        elif i==len(processed_text) - 1: # last word
            if processed_text[i][0] == processed_text[i-1][0]:
                if processed_text[i] not in alliterations:
                    alliterations.append((i,processed_text[i]))
        
        elif processed_text[i][0] == processed_text[i-1][0] or processed_text[i][0] == processed_text[i+1][0]:
            if processed_text[i] not in alliterations:
                alliterations.append((i,processed_text[i]))
    
    return alliterations

def phonetic_checker(split_text, alliterations):

    similar_sounds = ['c*k','v*w']
    f_ph = ['f*ph','ph*f']
    trigram_tuples = {}
    for i in range(len(split_text)-1):
        trigram_tuples[i] = split_text[i][0]+'*' + split_text[i+1][:2]
    
    # print(trigram_tuples)

    for i, trigram in trigram_tuples.items():
        if trigram[:-1] in similar_sounds or trigram[:-1:-1] in similar_sounds or trigram in f_ph:
            # print()
            if split_text[i] not in alliterations:
                alliterations.append((i,split_text[i]))

                if i == len(split_text) - 2:
                    if split_text[i+1] not in alliterations:
                        alliterations.append((i+1,split_text[i+1]))

    return alliterations

def detect_alliteration(text):
    # Comparing first alphabets of consecutive words to find alliterations 
    processed_text = preprocess(text).split(' ')
    alliterations = []
    
    alliterations = consecutive_word_checker(processed_text, alliterations) 
    alliterations = phonetic_checker(processed_text, alliterations)

    alliterations = list(map(lambda x: x[1],sorted(alliterations, key= lambda x: x[0])))
    # print(alliterations)
    return '-'.join(alliterations)


if __name__ == "__main__":
    text = input("Enter your sentence: ")
    # text = "Dan declares that he deserves to debate"
    # text = "the cruel king was kind in real life"
    print("Sentence:", text)
    print()
    alliteration = detect_alliteration(text)
    if alliteration != '':
        print("Words in the alliteration:", alliteration)
        print()
    else:
        print("No alliterations found!")