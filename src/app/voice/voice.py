"""
Is a table being bought by Ritika?
Perfect continuous tense
"""
from app.tense import tense_final
import nltk
# nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, pos_tag
import re

class Voice:
    def __init__(self, sentence): 
        self.text = sentence
    def voiceDetection(self):
        text = word_tokenize(sentence)
        tagged = pos_tag(text)
        print(tagged)
        verbs = []
        for i in tagged:
            if(i[1] in ['VBN', 'VBD', 'VBP', 'VBG', 'VBZ', 'MD', 'VB']):
                verbs.append(i)
        print(verbs)
        tenseOf = tense.tenseDetection(sentence)
        print(tenseOf)
        tenseOf = tenseOf.split()

        voice = ''

        if(tenseOf[0] == 'Present'):
            if(tenseOf[1] == 'Simple'):
                for i in range(len(verbs)):
                    if(re.search("is|am|are", verbs[i][0])):
                        voice = 'Passive'
                        break
                    elif(verbs[i][1] in ['VBP', 'VBZ']):
                        voice = 'Active'
                        break
            elif(tenseOf[1] == 'Continuous'):
                for i in range(len(verbs) - 1):
                    if(verbs[i][1] == 'VBG' and verbs[i + 1][1] == 'VBN'):
                        voice = 'Passive'
                        break
                    elif(verbs[i][1] in ['VBG']):
                        voice = 'Active'
                        break
            elif(tenseOf[1] == 'Perfect'):
                for i in range(len(verbs) - 1):
                    if(verbs[i + 1][0] == 'been' and verbs[i + 2][1] == 'VBN'):
                        voice = 'Passive'
                        break
                    elif(verbs[i + 1][1] in ['VBN']):
                        voice = 'Active'
                        break

        elif(tenseOf[0] == 'Past'):
            if(tenseOf[1] == 'Simple'):
                for i in range(len(verbs)):
                    if(re.search("was|were", verbs[i][0])):
                        voice = 'Passive'
                        break
                    elif(verbs[i][1] in ['VBD']):
                        voice = 'Active'
                        break
            elif(tenseOf[1] == 'Continuous'):
                for i in range(len(verbs) - 1, 0, -1):
                    if(verbs[i][1] == 'VBN'):
                        voice = 'Passive'
                        break
                    elif(verbs[i][1] in ['VBG']):
                        voice = 'Active'
                        break
            elif(tenseOf[1] == 'Perfect'):
                for i in range(len(verbs) - 1):
                    if(verbs[i + 1][0] == 'been' and verbs[i + 2][1] == 'VBN'):
                        voice = 'Passive'
                        break
                    elif(verbs[i + 1][1] in ['VBN']):
                        voice = 'Active'
                        break

        elif(tenseOf[0] == 'Future'):
            if(tenseOf[1] == 'Simple'):
                for i in range(len(verbs) - 1, 0, -1):
                    if(verbs[i][1] in ['VBD', 'VBN']):
                        voice = 'Passive'
                        break
                    elif(verbs[i][1] in ['VB']):
                        voice = 'Active'
                        break
            elif(tenseOf[1] == 'Perfect'):
                for i in range(len(verbs) - 1):
                    if(verbs[i + 1][0] == 'been' and verbs[i + 2][1] == 'VBN'):
                        voice = 'Passive'
                        break
                    elif(verbs[i + 1][1] in ['VBN']):
                        voice = 'Active'
                        break
        output = dict()
        output['sentence'] = sentence
        output['voice'] = voice
    def execute(self):
        # Driver function
        return self.voiceDetection()

if __name__ == "__main__":
    sentence = "Jack attended the program"
    voice_obj = Voice(sentence)
    #s = sim_obj.detect_similes()
    s1=voice_obj.execute()
    print(s1)
