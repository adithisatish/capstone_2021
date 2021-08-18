# Dataset obtained from https://github.com/ytsvetko/metaphor/tree/master/input

from operator import sub
from SPODetector import SPO
import pandas as pd 
import numpy as np
from sklearn.metrics import accuracy_score
import os

path = "\\".join(os.getcwd().split("\\")[:-3] + ['data'])
data = pd.read_csv(os.path.join(path, "svo.csv"))
# print(data.head())
paragraph = 1

d1 = list(data.sentence)
subjects = list(data.subject)
for i in range(len(subjects)):
    try:
        x = subjects[i][1]
    except Exception as e:
        subjects[i] = "****"
# print(subjects)
spo_obj = SPO(d1,paragraph)

spo_obj.detect_svo()

count = 0
i = 0
for sentence_dict in spo_obj.svo_list:
    try:
        subj = sentence_dict['triplets'][0]['Subject']
        if subjects[i] != "****":
            if subjects[i] in subj:
                count+=1
    except Exception as e:
        pass
    
    i+=1

print("Count - Subject:",count)
    

