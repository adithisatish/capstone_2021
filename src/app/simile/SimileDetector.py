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


class Simile:
    def __init__(self,text, paragraph = 0):
        self.text = text
        self.similes=[dict() for number in range(len(text))]
        self.paragraph = paragraph
    
    def detect_similes(self):
        index=0
        for list_index in range(len(self.text)):
            self.similes[index]['Sentence']=self.text[list_index]
            self.text[list_index] = re.sub('[^a-zA-Z0-9 \n\.]', '', self.text[list_index])
            self.similes[index]['Simile']=list()
            self.similes[index]['Explanation']=list()
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
                    if val!=1 and j!=0 and final[j-1][0] in ["As", 'as'] and ' '.join(tokenized_text[j-1:j+4]) in self.similes:
                        continue
                    if (val!=1 and final[j][1] in ['JJ','NNP','NNS','NN','PRP','RB']):
                            if(final[j+1][0] in ['As','as']):
                                if(final[j+2][1] in ['JJ',"NN","NNS","NNP",'PRP'] or final[j+3][1] in ['JJ',"NN","NNS","NNP",'PRP'] ):
                                    if val!=1 and j!=0 and final[j-1][0] in ["As, as"]:
                                        continue
                                    self.similes[index]['Simile'].append(' '.join(tokenized_text[j:j+4]))
                                    val=1
            index+=1
        #return self.similes
    
    def helper(self,sent, simile):
        result=[]
        words=simile.split()
        result1=[]
        tokenized_text=word_tokenize(sent)
        final=nltk.pos_tag(tokenized_text)
        for i in range(len(final)):
            if(final[i][1]!='DT' and final[i][0] not in ["like", "as"]):
                result.append(final[i])
        for i in range(len(result)):
            if(result[i][0] in words):
                result1.append(result[i])
        if("as" in simile):
            result1.append(0)
        if("like" in simile):
            result1.append(1)
        return result1
    
    def explanation(self):
        for k in range(len(self.similes)):
            if( len(self.similes[k]['Simile'])!=0):
                Sentence=self.similes[k]['Sentence']
                for j in range(len(self.similes[k]['Simile'])):
                    s=re.sub('[^a-zA-Z0-9 ]', '', self.similes[k]['Simile'][j])
                    ans=self.helper(Sentence,s)
                    for i in range(0,2):
                        ans[i]=list(ans[i]) #convert tuple to list
                    for i in range(0, 2):
                        if(ans[i][1] in ['VB','VBD','VBG','VBN','VBP','VBZ']):
                            ans[i][1]=" verb "
                        elif(ans[i][1] in ["NN","NNS","NNP"]):
                            ans[i][1]=" noun "
                        elif(ans[i][1]=="JJ"):
                            ans[i][1]=" adjective "
                        elif(ans[i][1]=="RB"):
                            ans[i][1]=" adverb "
                        elif(ans[i][1]=="PRP"):
                            ans[i][1]=" pronoun "
                    t1=ans[0][1]
                    w1=ans[0][0]
                    t2=ans[1][1]
                    w2=ans[1][0]
                    x="like"
                    if(ans[2]==0):
                        x="as"
                    Explanation="The sentence \"" + Sentence + "\" is a simile because it compares the"+t1+"\""+w1+"\""+" and the"+t2+"\""+w2+"\""+ " using the word "+"\""+x+"\""
                    self.similes[k]['Explanation'].append(Explanation)
            


    def display(self):

        for i in range(len(self.similes)):
            print("Sentence:", self.similes[i]['Sentence'])
            print("Similes:",self.similes[i]['Simile'])
            print("Explanation:",self.similes[i]['Explanation'])
            print("**************************")
            
    
    def execute(self):
        # Driver function
        self.detect_similes()
        self.explanation()
        #self.display()
        return self.similes

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

    
    sim_obj = Simile(text)
    s1=sim_obj.execute()
