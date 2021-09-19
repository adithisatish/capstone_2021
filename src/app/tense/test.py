import pandas as pd
from TenseDetector import Tenses

df = pd.read_csv('tense.csv')
#print(df.to_string()) 
sentences = df['sentence'].tolist()
expected = df['tense'].tolist()
count = 0
ten_obj = Tenses(sentences, 1)
result_dict = ten_obj.execute()
result_tense = []
for i in result_dict:
    result_tense.append(i['tense'])

count = 0
total = 0
for i in range(len(expected)):
    total += 1
    if(expected[i] != result_tense[i]):
        #print(sentences[i])
        #print("Expected: {0}, Observed: {1}".format(expected[i], result_tense[i]))
        count += 1

print("Total = {0}".format(total))
print("Wrong = {0}".format(count))
accuracy = (total-count)*100/total
print("Accuracy = {0}".format(accuracy))
#print(s1)
#print(sentences)
#print(expected)