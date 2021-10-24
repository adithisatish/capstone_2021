import pandas as pd
from VoiceDetector import Voice

df = pd.read_csv('voice.csv')
#print(df.to_string()) 
sentences = df['sentence'].tolist()
expected = df['voice'].tolist()
count = 0
voice_obj = Voice(sentences, 1)
result_dict = voice_obj.execute()
result_voice = []
for i in result_dict:
    result_voice.append(i['voice'])

count = 0
total = 0
print(len(expected))
print(len(result_voice))
for i in range(len(expected)):
    total += 1
    if(expected[i] != result_voice[i]):
        print(sentences[i])
        print("Expected: {0}, Observed: {1}".format(expected[i], result_voice[i]))
        count += 1

print("Total = {0}".format(total))
print("Wrong = {0}".format(count))
accuracy = (total-count)*100/total
print("Accuracy = {0}".format(accuracy))
#print(s1)
#print(sentences)
#print(expected)