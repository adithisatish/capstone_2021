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
        self.paragraph=paragraph
        self.count=0
        self.finalwords = [[0 for k in range(4)] for j in range(len(self.text))]
        foo='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alphabet=dict(enumerate(foo))
        
    def preprocess(self):
        slicedwords=[]
        lastwords=[]
        j=0
        for i in range(len(text)):
            self.text[i]=re.sub(r'(?<=[.,?;:!])(?=[^\s])', r' ', self.text[i]) 
            self.text[i] = re.sub('[^a-zA-Z0-9 \n]', '', self.text[i]) 
            text[i]=text[i].lower()
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
            if(x>4 and lastwords[i][x-3:x]!='ing'):
                k=len(lastwords[i])
                for a in range(k-3,1,-1):
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
            if(self.finalwords[i][3]==0):
                flag=0
                for j in range(i+1,len(self.finalwords)):
                    if(len(self.finalwords[i][1])>1):
                        for k in range(len(self.finalwords[i][1])):
                            list=pronouncing.rhymes(self.finalwords[i][1][k])
                            for k in range(len(list)):
                                if(len(self.finalwords[j][1])>1 and self.finalwords[j][2]!=1):
                                    for l in range(len(self.finalwords[j][1])):
                                        if(self.finalwords[j][1][l]==list[k]):
                                            self.finalwords[j][2]=1
                                            flag=1
                                            self.finalwords[j][3]=self.alphabet[self.count]
                                            
                                if(self.finalwords[j][1][0]==list[k] and self.finalwords[j][2]!=1):
                                    self.finalwords[j][2]=1
                                    flag=1
                                    self.finalwords[j][3]=self.alphabet[self.count]
                                    
                    if(len(self.finalwords[i][1])==1):
                        list=pronouncing.rhymes(self.finalwords[i][1][0]) 
                        if(self.finalwords[i][1][0]==self.finalwords[j][1][0]):
                            self.finalwords[j][2]=1
                            flag=1
                            self.finalwords[j][3]=self.alphabet[self.count]
                            
                        for k in range(len(list)):
                            if(len(self.finalwords[j][1])>1 and self.finalwords[j][2]!=1):
                                for l in range(len(self.finalwords[j][1])):
                                    if(self.finalwords[j][1][l]==list[k]):
                                        self.finalwords[j][2]=1
                                        flag=1
                                        self.finalwords[j][3]=self.alphabet[self.count]
                                        
                            if(self.finalwords[j][1][0]==list[k] and self.finalwords[j][2]!=1):
                                self.finalwords[j][2]=1
                                flag=1
                                self.finalwords[j][3]=self.alphabet[self.count]
            
                if(flag==1):
                    self.finalwords[i][3]=self.alphabet[self.count]
                    self.count+=1
        return self.count

    def eye_rhyme(self):  
        for x in range(len(self.finalwords)):
            counter=0
            for i in range(x+1,len(self.finalwords)): 
                k=len(self.finalwords[i][1][0])-1
                counter=0
                for j in range(len(self.finalwords[x][1][0])-1,0,-1):
                    if(self.finalwords[x][1][0][j]==self.finalwords[i][1][0][k] and k>0 and self.finalwords[x][1][0][len(self.finalwords[x][1][0])-3:len(self.finalwords[x][1][0])]!='ing'):
                        counter+=1
                        k=k-1
                    if(counter>1):
                        if(self.finalwords[x][3]==0 and self.finalwords[i][3]==0):
                            self.finalwords[x][3]=self.alphabet[self.count]
                            self.finalwords[i][3]=self.alphabet[self.count]
                            self.count+=1
                        counter=0
    def display(self):
        a=0
        foo='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(len(self.finalwords)):
            self.finalwords[i][2]=0
        for i in range(len(self.finalwords)):
            if(self.finalwords[i][3]==0):
                self.finalwords[i][3]=foo[a]
                a+=1
            else:
                if(self.finalwords[i][2]==0):
                    for j in range(i+1,len(self.finalwords)):
                        if(self.finalwords[j][3]==self.finalwords[i][3]):
                            self.finalwords[j][3]=foo[a]
                            self.finalwords[j][2]=1
                    self.finalwords[i][3]=foo[a]
                    a+=1
        rhymes=[dict() for number in range(len(self.text))]
        for i in range(len(self.text)):
            rhymes[i]['Line']=self.text[i]
            rhymes[i]['Letter']=self.finalwords[i][3]
            rhymes[i]['Word']=self.finalwords[i][1][0]

        for j in range(len(rhymes)):
            print("Line:",rhymes[j]['Line'])
            print("Letter:",rhymes[j]['Letter'])
            print("Word:",rhymes[j]['Word'])
            print("***************")
        return rhymes
            
    def execute(self):
        # Driver function
        self.preprocess()
        self.perfect_rhymes()
        self.eye_rhyme()
        self.identical_rhymes()
        return self.display()
        

if __name__ == "__main__":
    text=["There will come soft rain and the smell of the ground,","And swallows circling with their shimmering sound;","And frogs in the pools singing at night,",
          "And wild plum trees in tremulous white;","Robins will wear their feathery fire","Whistling their whims on a low fence-wire;",
          "And not one will know of the war, not one","Will care at last when it is done.","Not one would mind, neither bird nor tree,","If mankind perished utterly;",
         "And Spring herself, when she woke at dawn","Would scarcely know that we were gone."]
    
    
    rd_obj = RhymeScheme(text,1)
    rd=rd_obj.execute() 
   
