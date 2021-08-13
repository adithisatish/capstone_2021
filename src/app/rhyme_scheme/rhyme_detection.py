
# The idea for implementing rhyme scheme will follow the following steps-:
# i) The last word of each sentence of the poem will have to be extracted. 
# ii) One way to do this would be using tokenization.( Store the word occuring before ',' and '.')
# iii) After the last words are extracted, all possible combination of words formed using the end of the extracted words 
# eg. mocking-> [ird, bird, gbird, ngbird, ingbird, kingbird, ckingbird],
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
