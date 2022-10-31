
import math
import numpy as np

class TfidfVectorizer():
    def __init__(self):
        self.word_set = set()
        self.word_count_document = {}
        self.word_count = {}
        self.documents = []

    def fit(self, documents):
        self.documents = documents
        self.make_word_set()
        self.make_word_count_document()

    def fit_transform(self, documents):
        self.documents = documents
        self.make_word_set()
        self.make_word_count_document()
        value = []
        for document in documents:
            tmp = []
            self.make_word_count(document)
            N = len(document)
            for word in self.word_set:
                tfidf = self.tf(N, word) * self.idf(word)
                tmp.append(tfidf)
            value.append(tmp)
        return np.array(value)
    def transform(self, documents):
        value = []
        for document in documents:
            tmp = []
            self.make_word_count(document)
            N = len(document)
            for word in self.word_set:
                tfidf = self.tf(N, word) * self.idf(word)
                tmp.append(tfidf)
            value.append(tmp)   
        return np.array(value)
    def tf(self, N, word):
        occurance = self.word_count[word]
        return occurance / N
    
    def idf(self, word):
        return math.log(len(self.documents) / (1 + self.word_count[word]))

    def make_word_set(self):
        self.word_set = set()
        for document in self.documents:
            for word in document.split(" "):
                self.word_set.add(word)

    def make_word_count_document(self):
        self.word_count_document = {}
        for word in self.word_set:
            self.word_count_document[word] = 0
        for document in self.documents:
            tmp = set()
            for word in document.split(" "):
                tmp.add(word)
            for word in tmp:
                self.word_count_document[word] += 1
    
    def make_word_count(self, document):
        self.word_count = {}
        for word in self.word_set:
            self.word_count[word] = 0
        for word in document.split(" "):
            if word in self.word_set:
                self.word_count[word] += 1
if __name__ == '__main__':
    # combine_data()
    # create_stopwords()
    # print(get_data("the-thao"))
    combine_all_data()
    pass
