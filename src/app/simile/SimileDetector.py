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
    def __init__(self,text, paragraph = 0):
        self.text = text
        self.similes=[dict() for number in range(len(text))]
        self.paragraph = paragraph
    
    def detect_similes(self,text):
        index=0
        POS_tagged=[]
        for i in range(len(text)):
            self.similes[i]['Sentence']=text[i]
            text[i]=re.split(', |\n', text[i])
            self.similes[i]['Simile']=set()
            self.similes[i]['Explanantion']=[]
            for j in range(len(text[i])):
                text[i][j] = re.sub('[^a-zA-Z0-9 \.]', '', text[i][j])
                text[i][j] = text[i][j].replace(".", "")
                text[i][j]=text[i][j].lower()
                tokenized_text=word_tokenize(text[i][j])
                POS_tagged.append(nltk.pos_tag(tokenized_text))
        flag=0
        temp=[]
        for i in range(len(self.similes)):
            temp.append(re.sub('[^a-zA-Z0-9 \.]', '', self.similes[i]['Sentence']))
            temp[i]=temp[i].lower()
        for i in range(len(POS_tagged)):
            flag=0 
            key=-1
            for j in range(len(POS_tagged[i])): 
                if(POS_tagged[i][j][0]=='like'):
                    flag=1
                    key=j
                elif(POS_tagged[i][j][0]=='as' and key==-1):
                    flag=2
                    key=j
                if(key!=-1):
                    d_simile=POS_tagged[i][key][0]+' '
                    if( key+1<len(POS_tagged[i])):
                        d_simile=d_simile+POS_tagged[i][key+1][0]
                        if(key+2<len(POS_tagged[i])):
                            d_simile=d_simile+' '+POS_tagged[i][key+2][0]
                        if((key-1)>=0):
                            d_simile=POS_tagged[i][key-1][0]+' '+d_simile

            if(flag==1):# start check for like

                if(key-1>=0 and POS_tagged[i][key-1][1] in ['VB','VBD','VBG','VBN','VBP','VBZ'] ):
                    index=0
                    if(POS_tagged[i][key][0]=='like'):
                        if(POS_tagged[i][key+1][1]=='DT'):
                            if(key+2<len(POS_tagged[i]) and POS_tagged[i][key+2][1] in ["NN","NNS","NNP","JJ"]):
                                while(re.search(d_simile,temp[index])==None):
                                    index+=1
                                self.similes[index]['Simile'].add(d_simile)

                #rule 2
                if(key-1>=0 and POS_tagged[i][key-1][1] in ['VB','VBD','VBG','VBN','VBP','VBZ']):
                    index=0
                    if(POS_tagged[i][key][0]=='like'):
                        if(key+1<len(POS_tagged[i]) and POS_tagged[i][key+1][1] in ["NN","NNS","NNP","JJ","VBG"]):
                            while(re.search(d_simile,temp[index])==None):
                                index+=1
                            self.similes[index]['Simile'].add(d_simile)


                #rule 3
                if(key-1>=0 and POS_tagged[i][key-1][1] in ["RB","JJ","NN","NNS"]):
                    index=0
                    if(POS_tagged[i][key][0]=='like'):
                        if(key+1<len(POS_tagged[i]) and POS_tagged[i][key+1][1]=='DT'):
                            if(key+2<len(POS_tagged[i]) and POS_tagged[i][key+2][1] in ["NN","NNS","NNP","JJ"]):
                                while(re.search(d_simile,temp[index])==None):
                                    index+=1
                                self.similes[index]['Simile'].add(d_simile)


            if(flag==2):
                index=0
                if(key-1>=0 and key-1>=0 and POS_tagged[i][key-1][1] in ['JJ','NNP','NNS','NN','PRP','RB']):
                    if( POS_tagged[i][key][0]=='as'):
                        if( key+1<len(POS_tagged[i]) and POS_tagged[i][key+1][1] in ['JJ',"NN","NNS","NNP",'PRP']):
                            while(re.search(d_simile,temp[index])==None):
                                index+=1
                            self.similes[index]['Simile'].add(d_simile)
                        elif(key+2<len(POS_tagged[i]) and POS_tagged[i][key+2][1] in ['JJ',"NN","NNS","NNP",'PRP']):
                            while(re.search(d_simile,temp[index])==None):
                                index+=1 
                            self.similes[index]['Simile'].add(d_simile)


            if(flag==2):
                if(key+2<len(POS_tagged[i]) and POS_tagged[i][key+2][0]=='as'):
                        while(re.search(d_simile,temp[index])==None):
                            index+=1
                        self.similes[index]['Simile'].add(d_simile)
                            
        return self.similes
    
    def display(self):

        for i in range(len(self.similes)):
            print("Sentence:", self.similes[i]['Sentence'])
            print("Similes:",self.similes[i]['Simile'])
            print("**************************")
    
    def execute(self):
        # Driver function
        return self.detect_similes(self.text)

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
