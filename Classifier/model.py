from TfidfVectorizer import TfidfVectorizer
class NewsClassification():
    def __init__(self, model):
        self.tfidf_vectorizer = TfidfVectorizer()
        self.randomforest = RandomForestClassifier()
    def fit(self, data):
        
    def predict(self, data):
        tfidf_vectors = tfidf_vectorizer.transform(data)
        self.randomforest.fir

if __name__ == '__main__':
    randomforest = RandomForestClassifier()
    
    