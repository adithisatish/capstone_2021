# The idea for implementing rhyme scheme will follow the following steps-:
# i) The last word of each sentence of the poem will have to be extracted. 
# ii) One way to do this would be using tokenization.( Store the word occuring before ',' and '.')
# iii) After the last words are extracted, all possible combination of words formed using the end of the extracted words 
# need to be found. eg. mocking-> [ird, bird, gbird, ngbird, ingbird, kingbird, ckingbird],
# ignoring 'mockingbird', 'ockingbird', 'd',  and 'rd' for obvious reasons 
# These combination along with the original word would be stored in a dictionary holding all the extracted last word
# this dictionary would be checked for rhyming words using the pronuncing library.import pronouncing
import copy
import re
import math
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import pronouncing
flag=0
lastwords=[]
slicedwords=[]
n = 3


def identical_rhymes(lastwords):
    for i in range(len(lastwords)):
        for j in range(i+1,len(lastwords)):
            if(lastwords[i]==lastwords[j]):
                print("Identical rhymes are:", lastwords[i], lastwords[j])

                
                
def perfect_rhymes(finalwords):
    rset={}
    print(finalwords[0][2])

    for x in range(len(finalwords)):
        if(len(finalwords[x][1])>1):
            for i in range(len(finalwords[x][1])):
                list=pronouncing.rhymes(finalwords[x][1][i])
                for y in range(x+1,len(finalwords)):
                    for z in range(len(list)):
                        if(len(finalwords[y][1])>1):
                            for i in range(len(finalwords[y][1])):
                                if(list[z]==finalwords[y][1][i]):
                                    rset.update({finalwords[y][1][0]:finalwords[x][1][0]})
                                    if(finalwords[x][2]==0 and finalwords[y][2]==0):
                                        finalwords[x][2]:'A'
                                        finalwords[y][2]='A'
                                    print("Words that rhyme are:",finalwords[y][1][0],finalwords[x][1][0])
                        if(list[z]==finalwords[y][1][0]):
                            rset.update({list[z]:finalwords[x][1][0]})
                            if(finalwords[x][2]==0 and finalwords[y][2]==0):
                                        finalwords[x][2]:'A'
                                        finalwords[y][2]='A'
                            print("Words that rhyme are:",list[z],finalwords[x][1][0])
                    
        if(len(finalwords[x][1])==1): 
            list=pronouncing.rhymes(finalwords[x][1][0])
        for y in range(x+1,len(finalwords)):
            for z in range(len(list)):
                if(len(finalwords[y][1])>1):
                    for i in range(len(finalwords[y][1])):
                        if(list[z]==finalwords[y][1][i]):
                            rset.update({finalwords[y][1][0]:finalwords[x][1][0]})
                            if(finalwords[x][2]==0 and finalwords[y][2]==0):
                                        finalwords[x][2]:'A'
                                        finalwords[y][2]='A'
                            print("Words that rhyme are:",finalwords[y][1][0],finalwords[x][1][0])
                if(list[z]==finalwords[y][1][0]):
                    rset.update({list[z]:finalwords[x][1][0]})
                    if(finalwords[x][2]==0 and finalwords[y][2]==0):
                                        finalwords[x][2]:'A'
                                        finalwords[y][2]='A'
                    print("Words that rhyme are:",list[z],finalwords[x][1][0])
    print(finalwords)
                    

                    
                    
def eye_rhyme(lastwords):  #the sensitivity is set to 3
    for x in range(len(lastwords)):
        counter=0
        for i in range(x+1,len(lastwords)): 
            k=len(lastwords[i])-1
            counter=0
            for j in range(len(lastwords[x])-1,0,-1):
                if(lastwords[x][j]==lastwords[i][k] and k>0):
                    counter+=1
                    k=k-1
                if(counter>2):
                    print("Eye rhymes are:", lastwords[x], lastwords[i])
                    counter=0
                
                

if __name__ == "__main__":
    #text=["move, love. date,temperate. wind, behind.flies, enemies?dough, through."] 
    #text = ["Life gets faster everyday. often not giving us time to play. Hurry, chaos, lots of stress.  Tension leads to sleeplessness. When will this madness cease? Where is the free time? Where is peace? Im running, doing, till i drop. Give me buttons. Pause, mute. stop."]
    text = ["Hush little baby, don't say a word, Papa's gonna buy you a mockingbird. And if that mockingbird won't sing, Papa's gonna buy you a diamond ring. And if that diamond ring turns to brass, Papa's gonna buy you a looking glass. And if that looking glass gets broke, Papa's gonna buy you a billy goat. And if that billy goat won't pull, Papa's gonna buy you a cart and bull. And if that cart and bull turn over, Papa's gonna buy you a dog named rover. And if that dog named Rover won't bark. Papa's gonna buy you a horse and cart. And if that horse and cart fall down, You'll still be the sweetest little baby in town. "]
    #text= ["One little fishswam in his dish. He blew bubbles and made a wish. All he wanted was another fish to swim with him in his little dish. Another fish came one day to blow bubbles while they played. Two little fish blowing bubbles in the dish. Swimming around singing plish, plish, plish."]
    
    text[0]=re.sub(r'(?<=[.,?;:!])(?=[^\s])', r' ', text[0]) # if no space between special character, it is added here. 
    
    for i in range(len(text)):
        text[i] = text[i].rstrip()    #trailing whitespace is removed
    
    
    
    for sentence in text:               #tokenization starts here
        tokenized_text=word_tokenize(sentence)
        final=nltk.pos_tag(tokenized_text)
        j=0
        
    for i in range(len(final)):       
            if(final[i][0] in [',', '.' ,'?',';',':','!']):
                lastwords.insert(j, final[i-1][0])
                j+=1
    print(lastwords)  #here we add all the last words to a list 
    
    #in this part we do suffix extraction for longer words and append it all to a nested list 
    m=0
    finalwords = [[0 for k in range(n)] for j in range(len(lastwords))]
    for i in range(len(lastwords)):
        finalwords[i][0]=i
        finalwords[i][1]=lastwords[i]
        finalwords[i][2]=0
    for i in range(len(lastwords)):
        x=len((lastwords[i]))
        if(x>4 and lastwords[i][x-3:x]!='ing'): #exception handling(no suffix breaking for words that end in "ing"/large chances of false positives)
            k=len(lastwords[i])
            for a in range(k-3,1,-1):
                slicedwords.insert(m,lastwords[i][a:k])
                finalwords[i][1]=finalwords[i][1]+ ' ' + slicedwords[m]
                m+=1
    for y in range(len(finalwords)):
        finalwords[y][1]=finalwords[y][1].split()   #Suffixes are split and represented as words instead of strings
    
    
    #identical_rhymes(lastwords)
    
    
    #eye_rhyme(lastwords)
    
    perfect_rhymes(finalwords)

    
