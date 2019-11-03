import nltk
import time
from nltk.corpus import stopwords

import json
from math import log, sqrt
# default dict se usa para evitar crear una nueva entrada vacia de diccionario cada vez que haya una nueva palabra
from collections import defaultdict

#funcion para contar el numero de doc y el numero de terminos

terms = set()
tf = {}
query_and_terms = set()
doc_freq = {} # para cada termino, en cuantos documentos aparece


N = 20 # cantidad de docs
M = 22 #cantidad de terminos

def search_doc(id):
    return id

def do_query(query):
    query_terms_vector = stem_and_tokenize(query)
    file = open("test.json", "r")

    for i in range(N):
        j = file.readline()
        d = json.loads(j)
        s = stem_and_tokenize(d['text'])
        j = file.readline()
        j = file.readline()
        query_and_terms = query_terms_vector.intersection(terms)



def compute_terms():
    file = open("test.json", "r")

    for i in range(N):
        j = file.readline()
        doc = json.loads(j)
        tf[doc['id']] = {}
        s = stem_and_tokenize(doc['text'])
        for i in s:
            terms.add(i)
        j = file.readline()
        j = file.readline()
    file.close()


def term_frequency(term):
    file = open("test.json", "r")

    for i in range(N):
        j = file.readline()
        doc = json.loads(j)
        s = stem_and_tokenize(doc['text'])
        term_freq(term, s)
        j = file.readline()
        j = file.readline()
    file.close()


def stem_and_tokenize(text):
    tkn_list = nltk.word_tokenize(text)
    ps = nltk.stem.snowball.SnowballStemmer("spanish")
    stop_words = set(stopwords.words('spanish'))
    filtered = [w for w in tkn_list if w not in stop_words]

    my_result = set()
    for word in filtered:
        my_result.add(ps.stem(word))
    return my_result


def term_freq(term, doc):
    count  = 0
    for word in doc:
        if word == term:
            count = count + 1
    return count


def doc_freq(doc):
    query_terms_vector = stem_and_tokenize(doc)
    file = open("test.json", "r")
    length = 0
    for i in range(N):
        j = file.readline()
        d = json.loads(j)
        s = stem_and_tokenize(d['text'])
        file.readline()
        file.readline()
        query_and_terms = query_terms_vector.intersection(terms)
       ''' for word in doc_vector:
            frequency = doc_vector[word]
            score = tf_idf_score(word, frequency)
            doc_vector[word] = score
            length += score ** 2
        length = sqrt(length)
        for word in doc_vector:
            doc_vector[word] /= length'''
    file.close()

def tf_idf_score(term, doc):
    return log(1 + term_freq(term, doc)) * log(N / doc_freq[term])


compute_terms()
print(terms)
n  = str(input())
print(stem_and_tokenize(n))