#Are you coming to school? - Are is recognised as proper Noun

"""
TOKENS:
Past:   
        VBD verb, past tense took
        VBN verb, past participle taken
Present: 
        VBP verb, sing. present, non-3d take
        VBG verb, gerund/present participle taking
        VBZ verb, 3rd person sing. present takes
Future: 
        MD modal could, will

NN noun, singular 'desk'
NNS noun plural 'desks'
"""

"""
RULES:
Past:
    Past Simple: Second form of verb only (past)
    Past Continuous: was/were + verb + ing
    Past Perfect: Had + past partciple
    Past Perfect Continuous: Had been + verb + ing
Present:
    Present Simple: Verb + s/es
    Present Continuous: Is/am/are + verb + ing
    Present Perfect: Has/have + past partciple
    Present Perfect Continuous: Has/have + been + verb + ing
Future:
    Future Simple: Shall/will + verb
    Future continuous: Shall/will + be + verb + ing
    Future Perfect: Shall/will + have + past partciple
    Future Perfect Continuous: Shall/will + have + been + verb + ing

Verb Forms:
First Form: Verb
Second Form: Past 
Third Form: Past Participle
"""
import nltk
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, pos_tag
import re

sentence = ["Jack attended the program",
"Reena was waiting for my friends",
"Ahana was happy to hear the news",
"The players had played hockey in that field before it started to rain",
"I had been singing various kinds of songs for an hour",
"Bobby has given the book to Allen",
"The sci-fi movie is fantastic",
"Children love to play football",
"The lyricist narrates realistic songs",
"People are shopping in that market",
"We have shopped in this market",
"Rubina will join us in the meeting",
"We will be shopping in that market this Sunday",
"Rohini will have joined us at the meeting before you reach",
"He will have been shopping in that market before we come",
"I finished modifying XAI and tense"]

for j in sentence:
    print()
    print(j)
    text = word_tokenize(j)
    tagged = pos_tag(text)
    #print(tagged)

    verbs = []
    for i in tagged:
        if(i[1] in ['VBN', 'VBD', 'VBP', 'VBG', 'VBZ', 'MD', 'VB']):
            verbs.append(i)
    #print(verbs)

    for i in range(len(verbs)):
        if(len(verbs) >= 2):
            #past
            if(re.search("was|were", verbs[i][0]) and verbs[i+1][1] == 'VBG'):
                print("Past Continuous")
                break
            elif(re.search("had", verbs[i][0]) and re.search("been", verbs[i+1][0]) and verbs[i+2][1] == 'VBG'):
                print("Past Perfect Continuous")
                break
            elif(re.search("had", verbs[i][0]) and verbs[i+1][1] == 'VBN'):
                print("Past Perfect")
                break
            elif(verbs[i][1] == 'VBD'):
                print("Past Simple")
                break

            #present
            elif(re.search("is|am|are", verbs[i][0]) and verbs[i+1][1] == 'VBG'):
                print("Present Continuous")
                break
            elif(re.search("has|have", verbs[i][0]) and re.search("been", verbs[i+1][0]) and verbs[i+2][1] == 'VBG'):
                print("Present Perfect Continuous")
                break
            elif(re.search("has|have", verbs[i][0]) and verbs[i+1][1] == 'VBN'):
                print("Present Perfect")
                break
            elif(verbs[i][1] in ['VBP', 'VBZ']):
                print("Present Simple")
                break
            elif(verbs[i][1] == 'VBG'):
                print("Present Continuous")
                break

            #future
            elif(verbs[i][1] == 'MD'):
                if(re.search("be", verbs[i + 1][0]) and verbs[i+2][1] == 'VBG'):
                    print("Future Continuous")
                    break
                elif(re.search("has|have", verbs[i+1][0]) and re.search("been", verbs[i+2][0]) and verbs[i+3][1] == 'VBG'):
                    print("Future Perfect Continuous")
                    break
                elif(re.search("have", verbs[i + 1][0]) and verbs[i+2][1] == 'VBN'):
                    print("Future Perfect")
                    break
                else:
                    print("Future Simple")
                    break
        else:
            if(verbs[i][1] == 'VBD'):
                print("Past Simple")
                break
            elif(verbs[i][1] in ['VBP', 'VBZ']):
                print("Present Simple")
                break
            elif(verbs[i][1] == 'VBG'):
                print("Present Continuous")
                break
            elif(verbs[i][1] == 'MD'):
                print("Future Simple")
                break