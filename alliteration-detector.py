# Alliteration Detection 

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

# Function to detect alliteration 
def detect_alliteration(text):
    # Comparing first alphabets of consecutive words to find alliterations 

    processed_text = preprocess(text).split(' ')
    alliterations = []
    for i in range(len(processed_text)):
        if i==0: # first word
            if processed_text[i][0] == processed_text[i+1][0]:
                if processed_text[i] not in alliterations:
                    alliterations.append(processed_text[i])

        elif i==len(processed_text) - 1: # last word
            if processed_text[i][0] == processed_text[i-1][0]:
                if processed_text[i] not in alliterations:
                    alliterations.append(processed_text[i])
        
        elif processed_text[i][0] == processed_text[i-1][0] or processed_text[i][0] == processed_text[i+1][0]:
            if processed_text[i] not in alliterations:
                alliterations.append(processed_text[i])

    return ' '.join(alliterations)


if __name__ == "__main__":
    text = "Peter Piper Picked a Peck of Pickled Peppers"
    print("Sentence:", text)
    print()
    alliteration = detect_alliteration(text)
    if alliteration != '':
        print("Alliteration:", alliteration)
        print()
    else:
        print("No alliterations found!")
