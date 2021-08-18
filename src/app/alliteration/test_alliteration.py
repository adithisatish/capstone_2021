from numpy.lib.type_check import real
from AlliterationDetector import Alliteration
import pandas as pd 
from sklearn.metrics import accuracy_score
import os

path = "\\".join(os.getcwd().split("\\")[:-3] + ['data'])
# print(path)
data = pd.read_csv(os.path.join(path, "alliterations.csv"))
# data = pd.read_csv("dataset.csv")
# print(data.head())
paragraph = 1

sentences = list(data['Text'])
actual_letters = list(data['Letter'])

allit = Alliteration(sentences,paragraph)
alliterations = allit.detect_alliterations()
predicted_letters = []
double_allit = []

for i, alliteration in enumerate(alliterations):
    cur_letters = []
    for allit in alliteration["alliteration"]:
        cur_letters.append(allit['begins_with'])
    
    if len(cur_letters)==1:
        predicted_letters.append(cur_letters[0])
    elif len(cur_letters) == 0:
        predicted_letters.append('0')
    else:
        label = '-'.join(cur_letters)
        predicted_letters.append(label)
        double_allit.append((sentences[i],actual_letters[i],label))


print("Accuracy with respect to alliteration letter: {0:2f}%".format(float(accuracy_score(actual_letters, predicted_letters)*100)))
# print()
# print("Incorrectly Predicted:")
# for i in range(len(actual_letters)):
#     if actual_letters[i] != predicted_letters[i]:
#         print(sentences[i], actual_letters[i], predicted_letters[i])

k = 0
actual_alliterations = list(data["Alliteration"])
perc_word_detected = []
for i, alliteration in enumerate(alliterations):
    joined_alliteration = ""
    words_detected = 0
    for allit in alliteration["alliteration"]:
        joined_alliteration+=allit["joined"]
    
    real_allit = set(actual_alliterations[k].split('-'))
    predicted_allit = set(joined_alliteration.split('-'))
    words_detected = (1 - len(real_allit-predicted_allit)/len(real_allit))*100

    perc_word_detected.append(words_detected)

    k+=1

data['Percentage of Words Detected'] = perc_word_detected
# print(data.head())

print("Average percentage of words in the alliteration detected by the algorithm : {0}%".format(round(sum(perc_word_detected)/len(perc_word_detected),2)))
        