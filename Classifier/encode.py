from TfidfVectorizer import TfidfVectorizer
from sklearn.utils.sparsefuncs import mean_variance_axis
from preprocess import *
import pickle
def create_encoder():
    X, y = get_data("Data/data.json")

    X_train, X_test , y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=123,stratify=y)
    tfidf_vectorizer = TfidfVectorizer() 
    tfidf_train_vectors = tfidf_vectorizer.fit_transform(X_train)
    tfidf_test_vectors = tfidf_vectorizer.transform(X_test)
if __name__ == '__main__':
    create_encoder()
   
