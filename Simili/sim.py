
import copy
import math
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
flag=0
if __name__ == "__main__":
    f_1 = open("test.txt","r")
    ipt = f_1.readlines()
    f_1.close()
    words = [] 
    for i in range(len(ipt)):
        ipt[i] = ipt[i].strip()
        line = ipt[i].split()
        words.append(line)

    print(ipt)
    # For "like" occuring in the sentense
    for x in range(len(words[0])):
        #for y in range(len())
        #print(words[i][])
        if(words[0][x]=='like'):
            flag=1
    #Checking occurence of <verb> "like a" <noun>
    if flag==1:
        for i in range(len(ipt)):
            text=word_tokenize(ipt[i])
            final=nltk.pos_tag(text)
            for j in range(len(final)-3):
                if (final[j][1] in ['NN','NNS','MD','VB','VBD','VBG','VBN','VBP','VBZ']):
                    if(final[j+1][0]=='like'):
                        if(final[j+2][1]=='DT'):
                            if(final[j+3][1] in ["NN","NNS","NNP","JJ"]):
                                print("SIMILI FOUND, Phrase:", final[j][0],final[j+1][0],final[j+2][0],final[j+3][0])
    # For "as" occuring in the sentense 
    for i in range(len(words[0])):
         if (words[0][i] == "as" and words[0][i+2]=="as"):
            print(words, i)
            print("SIMILI FOUND, Phrase:",words[0][i], words[0][i+1], words[0][i+2], words[i+3],words[i+4])




