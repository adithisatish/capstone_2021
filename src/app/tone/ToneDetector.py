# save and load a file
# import pickle
# import sys
import os
import pandas as pd
# import numpy as np
# import os

# text preprocessing
from nltk import word_tokenize
from nltk.stem import PorterStemmer
# from nltk.corpus import stopwords
import re

# feature extraction / vectorization
from sklearn.feature_extraction.text import TfidfVectorizer

# classifiers
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.pipeline import Pipeline

# Importing explanability module
import eli5
from eli5.formatters import format_as_dict

class Tone:

    def __init__(self, text, paragraph = 0):
        self.text = text
        self.tones=[]
        self.paragraph = paragraph
        self.model = None
        self.vect = None
    
    def initialize_data(self):
        if __name__ != "__main__":
            df_train = pd.read_csv('app/tone/data/data_train.csv')
            df_test = pd.read_csv('app/tone/data/data_test.csv')
        else:
            df_train = pd.read_csv('data/data_train.csv')
            df_test = pd.read_csv('data/data_test.csv')

        data = pd.concat([df_train, df_test])

        X_train = df_train.Text
        X_test = df_test.Text

        y_train = df_train.Emotion
        y_test = df_test.Emotion

        class_names = ['joy', 'sadness', 'anger', 'neutral', 'fear']

        return (data,X_train, X_test, y_train, y_test)

    def preprocess_and_tokenize(self, data):    
    # remove html markup
        data = re.sub("(<.*?>)", "", data)

        # remove urls
        data = re.sub(r'http\S+', '', data)
        
        # remove hashtags
        data= re.sub(r"(#[\d\w\.]+)", '', data)

        # remove @names
        data= re.sub(r"(@[\d\w\.]+)", '', data)

        # remove punctuation and non-ascii digits
        data = re.sub("(\\W|\\d)", " ", data)
        
        # remove whitespaces
        data = data.strip()
        
        # tokenization with nltk
        data = word_tokenize(data)
        
        # stemming with nltk
        porter = PorterStemmer()
        stem_data = [porter.stem(word) for word in data]
            
        return stem_data

    def vectorize(self, data, X_train, X_test):
        # TFIDF, unigrams and bigrams
        vect = TfidfVectorizer(tokenizer=self.preprocess_and_tokenize, sublinear_tf=True, norm='l2', ngram_range=(1, 2))

        # fit on our complete corpus
        vect.fit_transform(data.Text)

        # transform testing and training datasets to vectors
        X_train_vect = vect.transform(X_train)
        X_test_vect = vect.transform(X_test)

        return [X_train_vect, X_test_vect, vect]

    def detect_tone(self):
        # Train and Test vectors
        data,X_train, X_test, y_train, y_test = self.initialize_data()
        X_train_vect, X_test_vect, vect = self.vectorize(data, X_train, X_test)

        # Naive Bayes
        # nb = MultinomialNB()
        # nb.fit(X_train_vect, y_train)
        # ynb_pred = nb.predict(X_test_vect)

        # Random Forest
        # rf = RandomForestClassifier(n_estimators=50)
        # rf.fit(X_train_vect, y_train)
        # yrf_pred = rf.predict(X_test_vect)

        # Logistic Regression
        # log = LogisticRegressionCV(random_state=42)
        log = LogisticRegression(solver='lbfgs', multi_class='auto', max_iter=200, random_state=42)
        log.fit(X_train_vect, y_train)
        # ylog_pred = log.predict(X_test_vect)

        feature_names = vect.get_feature_names()

        for sentence in self.text:
            sentence = [sentence]
            sentence_vector = vect.transform(sentence)[0]
            emo = log.predict(sentence_vector)[0]
            print(emo)

            e = eli5.explain_prediction(log, sentence_vector, feature_names = feature_names, targets = [emo], top = 10)
            # print(e)
            d = eli5.formatters.format_as_dict(e)
            print(d)

            # emotion = d['targets'][0]['target']

            l = d['targets'][0]['feature_weights']['pos']
            features = []
            for i in l:
                if i['feature'] == "<BIAS>":
                    continue
                else:
                    features.append(i['feature'])
            
            self.tones.append({"Sentence": sentence, "Tone":emo, "Explanation":features})
        
        return self.tones

        # Linear Support Vector Classifier
        #svc = LinearSVC(tol=1e-05)
        #svc.fit(X_train_vect, y_train)
        #ysvc_pred = svc.predict(X_test_vect)

        # Finding F1-score of each classifier
        # f1Scores = dict()
        # # clfs = {0:[ynb_pred, "NB"], 1:[yrf_pred, "RF"], 2:[ylog_pred, "LR"] , 3:[ysvc_pred, "SVC"]}
        # clfs = {0:[ynb_pred, "NB"], 1:[yrf_pred, "RF"], 2:[ylog_pred, "LR"]}
        # for i in range(3):
        #     f1Scores[i] = f1_score(y_test, clfs[i][0], average = "micro")
        
        # # Identifying the best classifier
        # max_key = max(f1Scores, key = lambda x : f1Scores[x])
        # print("Best classifier: ", clfs[max_key][1])

        # return [vect, svc, log]
        return [vect, log]

    def display(self):
        for i in range(len(self.tones)):
            print("Sentence:", self.tones[i]['Sentence'])
            print("Tone:",self.tones[i]['Tone'])
            print("Explanation:",self.tones[i]['Explanation'])
            print("**************************")
    
    def execute(self):
        # Driver function
        # self.serialize_data()
        return self.detect_tone()

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

    tone_obj = Tone(["She ran as fast as a horse"])
    # tone_obj.serialize_data()

    s1 = tone_obj.execute()
    print(tone_obj.tones)
    # s1 = tone_obj.display()