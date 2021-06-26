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
flag=0

def detect_similes(text):
    #text = text.replace(',', '')
    similes = []
    text = re.sub('[^a-zA-Z0-9 \n\.]', '', text)
    flag = 0
    val=0
    tokenized_text=word_tokenize(text)
    final=nltk.pos_tag(tokenized_text)
    #print("POS:",final)
        # print()
    words = text.split()
    
    
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
                            similes.append(' '.join(tokenized_text[j:j+4]))# final[j][0],final[j+1][0],final[j+2][0],final[j+3][0])
                            val=1
                    
                    elif final[j+2][1] in ["NN","NNS","NNP","JJ","VBG"]:
                        similes.append(' '.join(tokenized_text[j:j+3]))#final[j][0],final[j+1][0],final[j+2][0])
                        val=1
            
            elif final[j][1] in ["RB","JJ","NN","NNS"]:
                if(final[j+1][0] in ['like','Like']):
                    if(final[j+2][1]=='DT'):
                        if(final[j+3][1] in ["NN","NNS","NNP","JJ"]):
                            similes.append(' '.join(tokenized_text[j:j+4]))#final[j][0],final[j+1][0],final[j+2][0],final[j+3][0])
                            val=1
                            
                         
                            
    # For "as" occuring in the sentense 
    for i in range(len(words)-2):
         if (words[i] in ["as", "As"] and words[i+2] in ["as", "As"]):
            similes.append(' '.join(words[i:i+5]))
            val=1
    for j in range(len(final)-3):
        if (final[j][1] in ['JJ','NNP','NNS','NN','PRP','RB']):
                if(final[j+1][0] in ['As','as']):
                    if(final[j+2][1] in ['JJ',"NN","NNS","NNP",'PRP'] or final[j+3][1] in ['JJ',"NN","NNS","NNP",'PRP'] ):
                        similes.append(' '.join(tokenized_text[j:j+4]))# final[j][0],final[j+1][0],final[j+2][0],final[j+3][0])
                        val=1
    return (val, similes)

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

    path = "\\".join(os.getcwd().split("\\")[:-1] + ['data'])
    dataset = pd.read_csv(os.path.join(path, "similes.csv"))

    dataset["Simile"] = dataset["Simile"].replace({"Y":1, "N":0})

    predictions = {}
    predictions["Actual"] = list(dataset["Simile"])
    predictions["Predicted"] = [-1]*len(predictions["Actual"])

    k = 0
    for i in dataset["Sentence"]:
        val, similes = detect_similes(i)
        print(similes)
        predictions["Predicted"][k] = val
        k+=1
    
    # print(predictions)

    k = 0

    confusion_matrix = [[0,0],[0,0]]
    while k < len(predictions['Actual']):
        if predictions['Actual'][k] == 1 and predictions['Predicted'][k] == 1:
            confusion_matrix[0][0]+=1
        elif predictions['Actual'][k] == 1 and predictions['Predicted'][k] == 0:
            confusion_matrix[0][1]+=1
        elif predictions['Actual'][k] == 0 and predictions['Predicted'][k] == 1:
            confusion_matrix[1][0]+=1
        elif predictions['Actual'][k] == 0 and predictions['Predicted'][k] == 0:
            confusion_matrix[1][1]+=1
        k+=1

    accuracy = 100*((confusion_matrix[0][0] + confusion_matrix[1][1])/len(predictions['Actual']))
    precision = 100*(confusion_matrix[0][0]/(confusion_matrix[0][0] + confusion_matrix[1][0]))
    recall = 100*(confusion_matrix[0][0]/(confusion_matrix[0][0] + confusion_matrix[0][1]))
    f1_score = 2*precision*recall/(precision + recall)

    print("\n\nPerformance Metrics:")
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1_score)
    print("--------------------------------")
    # for i in range(len(text)):
    #     text[i] = text[i].rstrip()
    #     # text[i] = text[i].rstrip('.')
    #     # print(text[i])

    # # print(text)
    # print()

    # for sentence in text:
    #     detect_similes(sentence)
    print




