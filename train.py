from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
# from sklearn.feature_extraction.text import TfidfVectorizer
from TfidfVectorizer import TfidfVectorizer
from sklearn import metrics
from preprocess import *
import numpy as np
import pickle
import joblib



X, y = get_data("Data/data.json")

X_train, X_test , y_train, y_test = train_test_split(X, y, test_size=0.1,random_state=123,stratify=y)


def train():
    # tfidf_vectorizer = TfidfVectorizer() 
    # tfidf_train_vectors = tfidf_vectorizer.fit(X_train)
    # joblib.dump(tfidf_vectorizer, 'Classifier/vectorizer.joblib')
    tfidf_vectorizer = joblib.load('Classifier/vectorizer.joblib')
    tfidf_train_vectors = tfidf_vectorizer.transform(X_train)
    classifier = RandomForestClassifier()
    classifier.fit(tfidf_train_vectors,y_train)
    tfidf_test_vectors = tfidf_vectorizer.transform(X_test)
    y_pred = classifier.predict(tfidf_test_vectors)
    results = metrics.accuracy_score(y_test, y_pred)
    print(results)
    joblib.dump(classifier, 'Classifier/randomforest.joblib')
def pre(X=None, y=None):
    classifier = joblib.load('Classifier/randomforest.joblib')
    # tfidf_vectorizer = joblib.load('Classifier/vectorizer.joblib')
    tfidf_vectorizer = TfidfVectorizer() 
    tfidf_vectorizer.fit(X_train)
    # classifier = RandomForestClassifier()
    # classifier.fit(tfidf_train_vectors,y_train)
    # joblib.dump(tfidf_vectorizer, 'Classifier/vectorizer.joblib')
    if X == None:
        tfidf_test_vectors = tfidf_vectorizer.transform(X_test)
        y_pred = classifier.predict(tfidf_test_vectors)
        results = metrics.accuracy_score(y_test, y_pred)
        print(results)
    else:
        tfidf_test_vectors = tfidf_vectorizer.transform([clean_text(text) for text in X])
        y_pred = classifier.predict(tfidf_test_vectors)
        print(y_pred)
        if y != None:
            results = metrics.accuracy_score(y, y_pred)
            print(results)
if __name__ == '__main__':
    # train()
    # X, y = get_data('news_crawler/vietnamnet/data.json')
    pre()
    
    

  