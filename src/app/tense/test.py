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
    #print(i)
    total += 1
    if(expected[i] != result_tense[i]):
        print(sentences[i])
        print("Expected: {0}, Observed: {1}".format(expected[i], result_tense[i]))
        count += 1

print("Total = {0}".format(total))
print("Wrong = {0}".format(count))
accuracy = (total-count)*100/total
print("Accuracy = {0}".format(accuracy))
#print(s1)
#print(sentences)
#print(expected)

# aux > ccomp > advcl

#DONE - Gives both tenses - need to make explanation better
"""
When I saw him, he was playing chess
Expected: Past Continuous, Observed: Past Continuous and Past Simple

When I reached the station the train had started
Expected: Past Perfect, Observed: Past Perfect and Past Simple

I had done my exercise when Hari came to see me
Expected: Past Perfect, Observed: Past Perfect and Past Simple

I had written the letter before he arrived.
Expected: Past Perfect, Observed: Past Perfect and Past Simple

When Mr Mukerji came to the school in 1995, Mr Anand had already been teaching there for five years.
Expected: Past Perfect Continuous, Observed: Past Simple

"""

#FINAL INCORRECT
"""
Have you read 'Gulliver's Travels'?
Expected: Present Perfect, Observed: Present Simple

I’m sure Helen will get a first class
Expected: Future Simple, Observed: Present Simple

I am going to resign the job
Expected: Future Simple, Observed: Present Continuous

It is going to rain; look at those clouds
Expected: Future Simple, Observed: Present Simple and Present Continuous

Look! The cracker is going to explode
Expected: Future Simple, Observed: Present Continuous

We are about to have lunch.
Expected: Future Simple, Observed: Present Simple

Whenever prices goes up, customers buy less products.
Expected: Future Simple, Observed: Present Simple

Since winter is coming, I think I'll knit a warm sweater, because I'm always cold.
Expected: Future Simple, Observed: Present Simple and Future Simple

Accuracy = 111/119 = 93.27%
"""