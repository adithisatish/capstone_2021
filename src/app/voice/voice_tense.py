"""
Active: Circumstances will oblige me to go
Passive: I shall be obliged to go

"""

import nltk
# nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, pos_tag
import re
from nltk.corpus import stopwords

if __name__ != "__main__":
    import sys
    sys.path.append("..")
    from app.tense.TenseDetector import Tenses

class Voice:
    def __init__(self, text, paragraph = 0): 
        self.voice_list = []
        self.paragraph = paragraph # indicates whether a single sentence has been passed or not
        self.text = text
        #self.explanation = lambda beg, allit: "*Due to the occurrence of the same letter (or sound) (i.e **{0}**) in adjacent or closely connected words (excluding commonly used words like 'a', \"the\", etc), **{1}** is considered to be an alliteration.*".format(beg, allit)

    def preprocess_text(self, text):
        # Removal of stopwords
        # Conversion to lowercase
        # Removal of punctuation

        words = stopwords.words("english")    
        convert = lambda x: " ".join([i for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower()
        return convert(text)

    def preprocess_para(self):
        if self.paragraph == 1:
            preprocessed_para = sentence.split('.')
            #print(preprocessed_para)
            return preprocessed_para
        else:
            return [self.text]

    def voiceDetection(self, sentence):
        tense = Tenses(sentence)
        s = tense.execute()
        # print(s)
        tense = s[0]['tense']
        text = word_tokenize(sentence)
        tagged = pos_tag(text)
        print(tagged)
        verbs = []
        for i in tagged:
            if(i[1] in ['VBN', 'VBD', 'VBP', 'VBG', 'VBZ', 'MD', 'VB']):
                verbs.append(i)
        tense = tense.split()
        print(verbs)
        #print(tense)
        voice = ''

        if(tense != []):
            if(tense[0] == 'Present'):
                if(tense[1] == 'Simple'):
                    for i in range(len(verbs)):
                        if(verbs[i][0] in ['is', 'are', 'was', 'were']):
                            voice = 'Passive'
                            break
                        elif(verbs[i][1] in ['VBP', 'VBZ']):
                            voice = 'Active'
                            break
                elif(tense[1] == 'Continuous'):
                    length = len(verbs)
                    print(length)
                    if(length > 2):
                        for i in range(len(verbs) - 1):
                            if(verbs[i][1] == 'VBG' and verbs[i + 1][1] == 'VBN'):
                                voice = 'Passive'
                                break
                    else:
                        for i in range(len(verbs)):
                            if(verbs[i][1] in ['VBG']):
                                voice = 'Active'
                                break
                        
                elif(tense[1] == 'Perfect'):
                    for i in range(len(verbs) - 1):
                        if(verbs[i + 1][0] == 'been' and verbs[i + 2][1] == 'VBN'):
                            voice = 'Passive'
                            break
                        elif(verbs[i + 1][1] in ['VBN']):
                            voice = 'Active'
                            break

            elif(tense[0] == 'Past'):
                if(tense[1] == 'Simple'):
                    for i in range(len(verbs)):
                        print(verbs[i])
                        if(verbs[i][0] in ['is', 'are', 'was', 'were']):
                            voice = 'Passive'
                            break
                        elif(verbs[i][1] in ['VBD', 'VBN']):
                            voice = 'Active'
                            break
                elif(tense[1] == 'Continuous'):
                    for i in range(len(verbs) - 1, 0, -1):
                        if(verbs[i][1] == 'VBN'):
                            voice = 'Passive'
                            break
                        elif(verbs[i][1] in ['VBG']):
                            voice = 'Active'
                            break
                elif(tense[1] == 'Perfect'):
                    for i in range(len(verbs) - 1):
                        if(verbs[i + 1][0] == 'been' and verbs[i + 2][1] == 'VBN'):
                            voice = 'Passive'
                            break
                        elif(verbs[i + 1][1] in ['VBN']):
                            voice = 'Active'
                            break

            elif(tense[0] == 'Future'):
                if(tense[1] == 'Simple'):
                    for i in range(len(verbs) - 1, 0, -1):
                        print(verbs[i])
                        if(verbs[i][1] in ['VBD', 'VBN']):
                            voice = 'Passive'
                            break
                        elif(verbs[i][1] in ['VB']):
                            voice = 'Active'
                            break
                elif(tense[1] == 'Perfect'):
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
            output['explanation'] = ''
            return output
        
        else:
            output = dict()
            output['sentence'] = sentence
            output['voice'] = ''
            output['explanation'] = ''
            return output

    def detect_voice(self):
        # processed_text_list = self.preprocess_para()
        # print(processed_text_list)
        if self.paragraph == 1:
            for i in self.text:
                try:
                    #print(i)
                    result = self.voiceDetection(i)
                    #print(result)
                    sentence_voice = {"sentence": i, "voice": result['voice'], "explanation": result['explanation']}
                    self.voice_list.append(sentence_voice)
                    #print(self.voice_list)
                except Exception as e:
                    print("!! Text that caused error: {0}!!\n".format(i))
                    print(e)
        else:
            try: 
                result = self.voiceSpoDetection(self.text[0])
                sentence_voice = {"sentence": result['sentence'], "voice": result['voice'], "explanation": result['explanation']}
                self.voice_list.append(sentence_voice)
            except Exception as e:
                print("!! Text that caused error: {0}!!\n".format(result['sentence']))
                print(e)
        # print(self.voice_list)
        return self.voice_list

    def execute(self):
        # Driver function
        return self.detect_voice()

if __name__ == "__main__":
    from TenseDetector import Tenses

    sentence = ["I shall be obliged to go"]
    voice_obj = Voice(sentence, 1)
    s1=voice_obj.execute()
    print(s1)
