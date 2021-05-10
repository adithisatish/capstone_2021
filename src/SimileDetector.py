
import copy
import math
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
flag=0

def detect_similes(text):
    simile = 0
    flag = 0
    words = text.split()
    # For "like" occuring in the sentense
    for x in range(len(words)):
        #for y in range(len())
        #print(words[i][])
        if(words[x]=='like'):
            flag=1
    #Checking occurence of <verb> "like a" <noun>
    if flag==1:
        tokenized_text=word_tokenize(text)
        final=nltk.pos_tag(tokenized_text)
        # print("POS:",final)
        # print()
        for j in range(len(final)-3):

            # print(final[j], tokenized_text[j])
            
            if (final[j][1] in ['VB','VBD','VBG','VBN','VBP','VBZ']):
                # print(words[j-1])
                if(final[j+1][0]=='like'):
                    # print("YES")
                    if(final[j+2][1]=='DT'):
                        if(final[j+3][1] in ["NN","NNS","NNP","JJ"]):
                            simile = 1
                            print("SIMILE FOUND, Phrase:", ' '.join(tokenized_text[j:j+4]))# final[j][0],final[j+1][0],final[j+2][0],final[j+3][0])
                    
                    elif final[j+2][1] in ["NN","NNS","NNP","JJ"]:
                        simile = 1
                        print("SIMILE FOUND, Phrase:", ' '.join(tokenized_text[j:j+3]))#final[j][0],final[j+1][0],final[j+2][0])
            
            elif final[j][1] in ["NN","NNS","MD"]:
                if(final[j+1][0]=='like'):
                    # print("YES")
                    if(final[j+2][1]=='DT'):
                        if(final[j+3][1] in ["NN","NNS","NNP","JJ"]):
                            simile = 1
                            print("SIMILE FOUND, Phrase:", ' '.join(tokenized_text[j:j+4]))#final[j][0],final[j+1][0],final[j+2][0],final[j+3][0])
    
    # For "as" occuring in the sentence 

    # print(words)
    for i in range(len(words)):
        try:
            if words[i] == "as" and words[i+2] == "as":
                simile = 1
                print("SIMILE FOUND, Phrase:",' '.join(words[i:i+4]))
        except Exception as e:
            pass
    
    if simile == 0:
        print("No similes detected!")

if __name__ == "__main__":
    text = ["Rob was never as honest as Emily.","He paints like a rainbow in the sky.", "She is as pretty as a flock of birds.","This path meanders like a stream.",
    "In our eighth grade pageant, we shone like stars.",
    "Her voice sounds like nails on a chalkboard!",
    "After I received that 'A' on my spelling test, I thought I might soar like an eagle.",
    "My best friend sings like an angel.","I know the pathway like the back of my hand.",
    "You're as brave as a lion.","I like short hair.", "I really like you.","Does she like oranges?",
    "I'd like to see your sister.","Quite a few Americans like sushi.",
    "I can't imagine what he was thinking to hide a thing like that from you.",
    "He looked like a hard-working countryman just in from the backwoods."]
    
    for i in range(len(text)):
        text[i] = text[i].rstrip()
        # text[i] = text[i].rstrip('.')
        # print(text[i])

    # print(text)
    print()

    for sentence in text:
        detect_similes(sentence)




