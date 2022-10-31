from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
# from sklearn.feature_extraction.text import TfidfVectorizer
from TfidfVectorizer import TfidfVectorizer
from sklearn import metrics
from preprocess import *
import numpy as np
import pickle

X, y = get_data()

X_train, X_test , y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=123,stratify=y)
tfidf_vectorizer = TfidfVectorizer() 
tfidf_vectorizer.fit(X_train)
print("bruh")
tfidf_train_vectors = tfidf_vectorizer.transform(X_train)
tfidf_test_vectors = tfidf_vectorizer.transform(X_test)
print(tfidf_test_vectors.shape)
print(tfidf_train_vectors.shape)


classifier = RandomForestClassifier()
classifier.fit(tfidf_train_vectors,y_train)

y_pred = classifier.predict(tfidf_test_vectors)

results = metrics.accuracy_score(y_test, y_pred)
print(results)


# print(clean_queries)
# rep_queries = vectorizer.fit_transform(clean_queries)
# print(rep_queries.shape)
# rep_query, _ = mean_variance_axis(rep_queries, axis=0)
# print(rep_query.shape)
