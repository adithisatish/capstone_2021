import sys
import copy
import re
import math
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import pronouncing


class RhymeScheme:
    
    def __init__(self,text,paragraph):
        self.text=text
        self.og_text = list(text)
        self.paragraph=paragraph
        self.count=0
        self.finalwords = [[0 for k in range(4)] for j in range(len(self.text))]
        foo='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alphabet=dict(enumerate(foo))
        self.rhymes = []
        
    def preprocess(self):
        slicedwords=[]
        lastwords=[]
        j=0
        for i in range(len(self.text)):
            self.text[i]=re.sub(r'(?<=[.,?;:!])(?=[^\s])', r' ', self.text[i]) 
            self.text[i] = re.sub('[^a-zA-Z0-9 \n]', '', self.text[i]) 
            self.text[i]=self.text[i].lower()
            self.text[i]=self.text[i].rstrip()
            tokenized_text=word_tokenize(self.text[i])
            lastwords.append(tokenized_text[len(tokenized_text)-1])
        m=0

        for i in range(len(lastwords)):
            self.finalwords[i][0]=i
            self.finalwords[i][1]=lastwords[i]
            self.finalwords[i][2]=0
        for i in range(len(lastwords)):
            x=len((lastwords[i]))
            if(x>=4 and lastwords[i][x-3:x]!='ing'):
                k=len(lastwords[i])
                for a in range(k-3,0,-1):
                    slicedwords.insert(m,lastwords[i][a:k])
                    self.finalwords[i][1]=self.finalwords[i][1]+ ' ' + slicedwords[m]
                    m+=1
        for y in range(len(self.finalwords)):
            self.finalwords[y][1]=self.finalwords[y][1].split() 
        
    def identical_rhymes(self):
        for i in range(len(self.finalwords)):
            for j in range(i+1,len(self.finalwords)):
                if(self.finalwords[i][3]==0 and self.finalwords[j][3]==0 and self.finalwords[i][1]==self.finalwords[j][1]):
                    self.finalwords[j][3]=self.alphabet[self.count]
                    self.finalwords[i][3]=self.alphabet[self.count]
                    self.count+=1

    def perfect_rhymes(self):
        for i in range(len(self.finalwords)):
            flag=0
            if(self.finalwords[i][2]==0):
                list=pronouncing.rhymes(self.finalwords[i][1][0]) 
                for j in range(len(self.finalwords)): 
                    if(i!=j):
                        if(len(self.finalwords[j][1])>1):
                            for k in range(len(self.finalwords[j][1])):
                                for l in range(len(list)):
                                    if(self.finalwords[j][1][k]==list[l]): 
                                        if(self.finalwords[j][2]==1):
                                            self.finalwords[i][3]=self.finalwords[j][3]
                                            self.finalwords[i][2]=1
                                        else:
                                            self.finalwords[j][3]=self.alphabet[self.count]
                                            self.finalwords[j][2]=1
                                            flag=1

                        else:
                            for k in range(len(list)):
                                if(self.finalwords[j][1][0]==list[k]):
                                    if(self.finalwords[j][2]==1):
                                        self.finalwords[i][3]=self.finalwords[j][3]
                                        self.finalwords[i][2]=1
                                    else:
                                        self.finalwords[j][3]=self.alphabet[self.count]
                                        self.finalwords[j][2]=1
                                        flag=1
            if(flag==1):
                self.finalwords[i][3]=self.alphabet[self.count]
                self.finalwords[i][2]=1
                self.count+=1
            

    def eye_rhyme(self):  
        for x in range(len(self.finalwords)):
            if(self.finalwords[x][2]==0 and self.finalwords[x][1][0][len(self.finalwords[x][1][0])-3:len(self.finalwords[x][1][0])]!='ing'): #only check if the word hasn't been tagged yet. 
                for i in range(len(self.finalwords)): #start the check from the beginning.
                    counter= 0
                    if(i!=x): #we dont to check word against the same word
                        k=len(self.finalwords[x][1][0])-1
                        for j in range(len(self.finalwords[i][1][0])-1,len(self.finalwords[i][1][0])-4,-1): #check only the last 4 words 
                            if(k>=0 and j>=0 and self.finalwords[x][1][0][k]==self.finalwords[i][1][0][j]):
                                counter+=1
                            k-=1;
                        if(counter>=3):
                            if(self.finalwords[i][2]==0 and self.finalwords[x][2]==0):
                                self.finalwords[x][3]=self.alphabet[self.count] 
                                self.finalwords[i][3]=self.finalwords[x][3]
                                self.finalwords[i][2]=1
                                self.finalwords[x][2]=1
                                self.count+=1
                            elif(self.finalwords[i][2]!=0):
                                self.finalwords[x][3]=self.finalwords[i][3]
                                self.finalwords[x][2]=1
                                
    def display(self):
        for j in range(len(self.rhymes)):
            print("Line:",self.rhymes[j]['Line'])
            print("Letter:",self.rhymes[j]['Letter'])
            print("Word:",self.rhymes[j]['Word'])
            print("***************")        

    def detect_rhyme_scheme(self):
        a=0
        foo='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(len(self.finalwords)):
            self.finalwords[i][2]=0
        for i in range(len(self.finalwords)):
            if(self.finalwords[i][3]==0):
                self.finalwords[i][3]=foo[a]
                self.finalwords[i][2]=1
                a+=1
            else:
                if(self.finalwords[i][2]==0):
                    for j in range(i+1,len(self.finalwords)):
                        if(self.finalwords[j][3]==self.finalwords[i][3] and self.finalwords[j][2]==0):
                            self.finalwords[j][3]=foo[a]
                            self.finalwords[j][2]=1
                    self.finalwords[i][3]=foo[a]
                    self.finalwords[i][2]=1
                    a+=1
        
        # self.create_rhyme_dict()
        self.rhymes=[dict() for number in range(len(self.text))]
        
        for i in range(len(self.text)):
            self.rhymes[i]['Line']=self.og_text[i]
            self.rhymes[i]['Letter']=self.finalwords[i][3]
            self.rhymes[i]['Word']=self.finalwords[i][1][0]

        
        return self.rhymes
            
    def execute(self):
        # Driver function
        # print("Execute - RS")
        self.preprocess()
        self.perfect_rhymes()
        self.eye_rhyme()
        self.identical_rhymes()
        return self.detect_rhyme_scheme()
        

if __name__ == "__main__":
    
    text=["Hush, little baby, don’t say a word,",
        "Papa’s gonna buy you a mockingbird.",

        "And if that mockingbird don’t sing,",
        "Papa’s gonna buy you a diamond ring.",

        "And if that diamond ring turn brass,",
        "Papa’s gonna buy you a looking glass.",

        "And if that billy goat don’t pull,",
        "Papa’s gonna buy you a cart and bull.",

        "And if that cart and bull turn over,",
        "Papa’s gonna buy you a dog named Rover.",

        "And if that dog named Rover won’t bark.",
        "Papa’s gonna to buy you and horse and cart.",

        "And if that horse and cart fall down,",
        "Well you’ll still be the sweetest little baby in town."]

    rd_obj = RhymeScheme(text,1)
    rd=rd_obj.execute() 
