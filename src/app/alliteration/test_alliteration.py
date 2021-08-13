from AlliterationDetector import Alliteration
import pandas as pd 
from sklearn.metrics import accuracy_score
import os

path = "\\".join(os.getcwd().split("\\")[:-2] + ['data'])
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


print("Accuracy: {0:2f}%".format(float(accuracy_score(actual_letters, predicted_letters)*100)))
print()
print("Incorrectly Predicted:")
for i in range(len(actual_letters)):
    if actual_letters[i] != predicted_letters[i]:
        print(sentences[i], actual_letters[i], predicted_letters[i])