import re
import copy
import math
import nltk
from nltk import data
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import os
import sys
import pandas as pd
import requests
flag=0


class Similes:
    def __init__(self,text):
        self.text = text
        self.similes=[dict() for number in range(len(text))]
    
    def detect_similes(self):
        index=0
        for list_index in range(len(text)):
            self.similes[index]['Sentense']=text[list_index]
            text[list_index] = re.sub('[^a-zA-Z0-9 \n\.]', '', text[list_index])
            self.similes[index]['Simile']=list()
            flag=0
            val=0
            tokenized_text=word_tokenize(self.text[list_index])
            final=nltk.pos_tag(tokenized_text)
            words = self.text[list_index].split()

        # For "like" occuring in the sentense
            for x in range(len(words)):
                if(words[x]in ['like','Like']):
                    flag=1
            if flag==1:
                for j in range(len(final)-3):
                    if (final[j][1] in ['VB','VBD','VBG','VBN','VBP','VBZ']):
                        if(final[j+1][0]in ['like','Like']):
                            if(final[j+2][1]=='DT'):
                                if(final[j+3][1] in ["NN","NNS","NNP","JJ"]):
                                    self.similes[index]['Simile'].append(' '.join(tokenized_text[j:j+4]))
                                    val=1

                            elif final[j+2][1] in ["NN","NNS","NNP","JJ","VBG"]:
                                self.similes[index]['Simile'].append(' '.join(tokenized_text[j:j+3]))
                                val=1

                    elif final[j][1] in ["RB","JJ","NN","NNS"]:
                        if(final[j+1][0] in ['like','Like']):
                            if(final[j+2][1]=='DT'):
                                if(final[j+3][1] in ["NN","NNS","NNP","JJ"]):
                                    self.similes[index]['Simile'].append(' '.join(tokenized_text[j:j+4]))
                                    val=1

            # For "as" occuring in the sentense 
            if flag==0:
                for i in range(len(words)-2):
                    if (words[i] in ["as", "As"] and words[i+2] in ["as", "As"]):
                        self.similes[index]['Simile'].append(' '.join(tokenized_text[i:i+5]))
                        val=1
                for j in range(len(final)-3):
                    if val!=1 and j!=0 and final[j-1][0] in ["As", 'as'] and ' '.join(tokenized_text[j-1:j+4]) in similes:
                        continue
                    if (val!=1 and final[j][1] in ['JJ','NNP','NNS','NN','PRP','RB']):
                            if(final[j+1][0] in ['As','as']):
                                if(final[j+2][1] in ['JJ',"NN","NNS","NNP",'PRP'] or final[j+3][1] in ['JJ',"NN","NNS","NNP",'PRP'] ):
                                    if val!=1 and j!=0 and final[j-1][0] in ["As, as"]:
                                        continue
                                    self.similes[index]['Simile'].append(' '.join(tokenized_text[j:j+4]))
                                    val=1
            index+=1
        return self.similes
    
    def display(self):

        for i in range(len(self.similes)):
            print("Sentence:", self.similes[i]['Sentense'])
            print("Similes:",self.similes[i]['Simile'])
            print("**************************")
            
    
    def execute(self):
        # Driver function
        return self.detect_similes()

if __name__ == "__main__":
    text = ["Rob was never as honest as Emily.","He paints like a rainbow in the sky.", "She is as pretty as a flock of birds.","This path meanders like a stream.",
    "In our eighth grade pageant, we shone like stars.",
    "Her voice sounds like nails on a chalkboard!",
    "After I received that 'A' on my spelling test, I thought I might soar like an eagle.",
    "My best friend sings like an angel.","I know the pathway like the back of my hand.",
    "You're as brave as a lion.","I like short hair.", "I really like you.","Does she like oranges?",
    "I'd like to see your sister.","Quite a few Americans like sushi.",
    "I can't imagine what he was thinking to hide a thing like that from you.",
    "He looked like a hard-working countryman just in from the backwoods.",
           "She ran like the wind, swam like a fish"]

    
    sim_obj = Similes(text)
    s1=sim_obj.execute()
    s1=sim_obj.display()
