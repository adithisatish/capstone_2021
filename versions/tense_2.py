import nltk
# nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, pos_tag
import re

def determine_tense_input(sentence):
    text = word_tokenize(sentence)
    tagged = pos_tag(text)
    #print(tagged)
    tense = {}
    tense["future"] = [len([word for word in tagged if word[1] == "MD"]), [word for word in tagged if word[1] == "MD"]]
    tense["past"] = [len([word for word in tagged if word[1] in ["VBD", "VBN"]]), [word for word in tagged if word[1] in ["VBD", "VBN"]]]
    tense["present"] = [len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]]), [word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]]]
    return(tense)

sentence = "Heena has sung"
text = word_tokenize(sentence)
tagged = pos_tag(text)
print(tagged)
tense_dict = determine_tense_input(sentence)

max = 0
tense = ''
for i in tense_dict:
    if tense_dict[i][0] > max:
        tense = i
        max = tense_dict[i][0]

#PAST TENSE
if(tense == "past"):
    flag = 0
    for i in range(len(tagged)-1):
        if re.search("was|were", tagged[i][0]) and re.search("ing$", tagged[i+1][0]):
            print("Past Continuous")
            print("Explanation: '" + tagged[i][0] + " " + tagged[i+1][0] + "' is in the form of 'was/were + verb + ing' ")
            flag = 0
            break
        elif tagged[i][0] == "had" and tagged[i+1][0] == "been" and re.search("ing$", tagged[i+2][0]):
            print("Past Perfect Continuous")
            print("Explanation: '" + tagged[i][0] + " " + tagged[i+1][0] + " " + tagged[i+2][0] + "' is in the form of 'had been + verb + ing'")
            flag = 0
            break
        elif tagged[i][0] == "had" and tagged[i+1][1] in ["VBD", "VBN"]:
            print("Past Perfect")
            print("Explanation: '" + tagged[i][0] + " " + tagged[i+1][0] + "' is in the form of 'had + third form of verb'")
            flag = 0
            break
        else:
            flag = 1
    if flag == 1:
        print("Past Simple")
        print("Explanation: The verb '" + tense_dict["past"][1][0][0]+ "' is in its second form")


#PRESENT
elif(tense == "present"):
    flag = 0
    for i in range(len(tagged)-1):
        if re.search("is|am|are", tagged[i][0]) and re.search("ing$", tagged[i+1][0]):
            print("Present Continuous")
            print("Explanation: '" + tagged[i][0] + " " + tagged[i+1][0] + "' is in the form of 'is/am/are + verb + ing' ")
            flag = 0
            break
        elif tagged[i][0] == "has|have" and tagged[i+1][0] == "been" and re.search("ing$", tagged[i+2][0]):
            print("Past Perfect Continuous")
            print("Explanation: '" + tagged[i][0] + " " + tagged[i+1][0] + " " + tagged[i+2][0] + "' is in the form of 'had been + verb + ing'")
            flag = 0
            break
        elif tagged[i][0] == "had" and tagged[i+1][1] in ["VBD", "VBN"]:
            print("Past Perfect")
            print("Explanation: '" + tagged[i][0] + " " + tagged[i+1][0] + "' is in the form of 'had + third form of verb'")
            flag = 0
            break
        else:
            flag = 1
    if flag == 1:
        print("Past Simple")
        print("Explanation: The verb '" + tense_dict["past"][1][0][0]+ "' is in its second form")


print(tense_dict)


