# save and load a file
import pickle
import sys
import os

# Importing explanability module
import eli5
from eli5.formatters import format_as_dict

if __name__ != "__main__":
    sys.path.append("..")

class Tone:

    def __init__(self, text, paragraph = 0):
        self.text = text
        self.tones=[dict() for number in range(len(text))]
        self.paragraph = paragraph

    def detect_tone(self, text):
        # Loading models and vectorizer
        if __name__ != "__main__":
            # print(os.getcwd())
            # s = "app/tone/models/tfidf_svc.sav"
            l = os.path.join(os.getcwd(),"app\\tone\\models\\tfidf_lr.sav")
            v = os.path.join(os.getcwd(),"app/tone/vectorizers/tfidf.sav")

            print("\n\nLog:", l)
        else:
            # s = "models/tfidf_svc.sav"
            l = "models/tfidf_lr.sav"
            v = "vectorizers/tfidf.sav"

        # svc = pickle.load(open(s, 'rb'))
        f = open("D:\PESU\capstone_2021\src\\app\\tone\\models\\tfidf_lr.sav", 'rb')
        
        
        log = pickle.load(open("D:\PESU\capstone_2021\src\\app\\tone\\models\\tfidf_lr.sav", 'rb'))
        vect = pickle.load(open("D:\PESU\capstone_2021\src\\app\\tone\\vectorizers\\tfidf.sav", 'rb'))

        # Get feature names
        feature_names = vect.get_feature_names()

        for sentence in text:
            emo = log.predict(sentence)[0]

            sentence_vector = vect.transform(sentence)
            e = eli5.explain_prediction(log, sentence_vector, feature_names = feature_names, targets = [emo], top = 10)
            d = format_as_dict(e)

            emotion = d['targets'][0]['target']

            l = d['targets'][0]['feature_weights']['pos']
            features = []
            for i in l:
                if i['feature'] == "<BIAS>":
                    continue
                else:
                    features.append(i['feature'])

    def display(self):
        for i in range(len(self.tones)):
            print("Sentence:", self.tones[i]['Sentence'])
            print("Tone:",self.tones[i]['Tone'])
            print("Explanation:",self.tones[i]['Explanation'])
            print("**************************")
    
    def execute(self):
        # Driver function
        return self.detect_tone(self.text)

if __name__ == "__main__":
    text = ["Rob was never as honest as Emily.","He paints like a rainbow in the sky.", "She is as pretty as a flock of birds.","This path meanders like a stream.",
    "In our eighth grade pageant, we shone like stars.",
    "Her voice sounds like nails on a chalkboard!",
    "After I received that 'A' on my spelling test, I thought I might soar like an eagle.",
    "My best friend sings like an angel.","I know the pathway like the back of my hand.",
    "You're as brave as a lion.","I like short hair.", "I really like you.","Does she like oranges?",
    "I'd like to see your sister.","Quite a few Americans like sushi.",
    "I can't imagine what he was thinking to hide a thing like that from you.",
    "He looked like a hard-working countryman just in from the backwoods.",
           "She ran like the wind, swam like a fish"]

    tone_obj = Tone(text)

    s1 = tone_obj.execute()
    s1 = tone_obj.display()