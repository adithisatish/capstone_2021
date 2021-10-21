import pandas as pd
import numpy as np

# text preprocessing
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re

# plots and metrics
#import matplotlib.pyplot as plt
from sklearn.metrics import f1_score

# feature extraction / vectorization
from sklearn.feature_extraction.text import TfidfVectorizer

# classifiers
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

# save and load a file
import pickle

df_train = pd.read_csv('data/data_train.csv')
df_test = pd.read_csv('data/data_test.csv')

data = pd.concat([df_train, df_test])

X_train = df_train.Text
X_test = df_test.Text

y_train = df_train.Emotion
y_test = df_test.Emotion

class_names = ['joy', 'sadness', 'anger', 'neutral', 'fear']

def preprocess_and_tokenize(data):    
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

def vectorize(data):
    # TFIDF, unigrams and bigrams
    vect = TfidfVectorizer(tokenizer=preprocess_and_tokenize, sublinear_tf=True, norm='l2', ngram_range=(1, 2))

    # fit on our complete corpus
    vect.fit_transform(data.Text)

    # transform testing and training datasets to vectors
    X_train_vect = vect.transform(X_train)
    X_test_vect = vect.transform(X_test)

    return [X_train_vect, X_test_vect, vect]

def classifiers():
    # Train and Test vectors
    X_train_vect, X_test_vect, vect = vectorize(data)

    # Naive Bayes
    nb = MultinomialNB()
    nb.fit(X_train_vect, y_train)
    ynb_pred = nb.predict(X_test_vect)

    # Random Forest
    rf = RandomForestClassifier(n_estimators=50)
    rf.fit(X_train_vect, y_train)
    yrf_pred = rf.predict(X_test_vect)

    # Logistic Regression
    log = LogisticRegression(solver='lbfgs', multi_class='auto', max_iter=200)
    log.fit(X_train_vect, y_train)
    ylog_pred = log.predict(X_test_vect)

    # Linear Support Vector Classifier
    svc = LinearSVC(tol=1e-05)
    svc.fit(X_train_vect, y_train)
    ysvc_pred = svc.predict(X_test_vect)

    # Finding F1-score of each classifier
    f1Scores = dict()
    clfs = {0:[ynb_pred, "NB"], 1:[yrf_pred, "RF"], 2:[ylog_pred, "LR"] , 3:[ysvc_pred, "SVC"]}
    for i in range(4):
        f1Scores[i] = f1_score(y_test, clfs[i][0], average = "micro")
    
    # Identifying the best classifier
    max_key = max(f1Scores, key = lambda x : f1Scores[x])
    print("Best classifier: ", clfs[max_key][1])

    return [vect, svc, log]

def serialize_data():
    # Retreving relevant data to be serialized
    vect, svc, log = classifiers()

    # Creating pipelines for models
    svc_model = Pipeline([("tfidf", vect), ("clf", svc),])
    lr_model = Pipeline([("tfidf", vect), ("clf", log),])

    # saving the models
    s = "C:/Users/91974/OneDrive/Desktop/models/tfidf_svc.sav"
    l = "C:/Users/91974/OneDrive/Desktop/models/tfidf_lr.sav"
    pickle.dump(svc_model, open(s, 'wb'))
    pickle.dump(lr_model, open(l, 'wb'))

    # saving the vectorizer
    v = "C:/Users/91974/OneDrive/Desktop/vectorizers/tfidf.sav"
    pickle.dump(vect, open(v, 'wb'))

serialize_data()