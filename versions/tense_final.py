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
    Past Simple: Second form of verb only (past) (VBD)
    Past Continuous: was/were + verb + ing (VBG)
    Past Perfect: Had + past partciple (VBN)
    Past Perfect Continuous: Had been + verb + ing (VBG)
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

def tenseDetection(sentence):
    tense = ""
    print()
    print(sentence)
    text = word_tokenize(sentence)
    tagged = pos_tag(text)
    print(tagged)

    verbs = []
    for i in tagged:
        if(i[1] in ['VBN', 'VBD', 'VBP', 'VBG', 'VBZ', 'MD', 'VB']):
            verbs.append(i)
    print(verbs)

    for i in range(len(verbs)):
        if(len(verbs) >= 2):
            #past
            if(re.search("was|were", verbs[i][0]) and verbs[i+1][1] == 'VBG'):
                tense = "Past Continuous"
                break
            elif(re.search("had", verbs[i][0]) and re.search("been", verbs[i+1][0]) and verbs[i+2][1] == 'VBG'):
                tense = "Past Perfect Continuous"
                break
            elif(re.search("had", verbs[i][0]) and verbs[i+1][1] == 'VBN'):
                tense = "Past Perfect"
                break
            elif(verbs[i][1] == 'VBD'):
                tense = "Past Simple"
                break

            #present
            elif(re.search("is|am|are", verbs[i][0]) and verbs[i+1][1] == 'VBG'):
                tense = "Present Continuous"
                break
            elif(re.search("has|have", verbs[i][0]) and re.search("been", verbs[i+1][0]) and verbs[i+2][1] == 'VBG'):
                tense = "Present Perfect Continuous"
                break
            elif(re.search("has|have", verbs[i][0]) and verbs[i+1][1] == 'VBN'):
                tense = "Present Perfect"
                break
            elif(verbs[i][1] in ['VBP', 'VBZ']):
                tense = "Present Simple"
                break
            elif(verbs[i][1] == 'VBG'):
                tense = "Present Continuous"
                break

            #future
            elif(verbs[i][1] == 'MD'):
                if(re.search("be", verbs[i + 1][0]) and verbs[i+2][1] == 'VBG'):
                    tense = "Future Continuous"
                    break
                elif(re.search("has|have", verbs[i+1][0]) and re.search("been", verbs[i+2][0]) and verbs[i+3][1] == 'VBG'):
                    tense = "Future Perfect Continuous"
                    break
                elif(re.search("have", verbs[i + 1][0]) and verbs[i+2][1] == 'VBN'):
                    tense = "Future Perfect"
                    break
                else:
                    tense = "Future Simple"
                    break
        else:
            if(verbs[i][1] == 'VBD'):
                tense = "Past Simple"
                break
            elif(verbs[i][1] in ['VBP', 'VBZ']):
                tense = "Present Simple"
                break
            elif(verbs[i][1] == 'VBG'):
                tense = "Present Continuous"
                break
            elif(verbs[i][1] == 'MD'):
                tense = "Future Simple"
                break
    return tense

"""
sentence = "A table is being bought by ritika"
print(tenseDetection(sentence))
"""

