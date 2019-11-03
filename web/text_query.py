import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import math
import json
import numpy as np


# ---------------------------------------------BEGIN-OF-FUNCTIONS-------------------------------------------------------
def list_stem_and_tokenize(text):
    tkn_list = nltk.word_tokenize(text)
    ps = nltk.stem.snowball.SnowballStemmer('spanish')
    stop_words = stopwords.words('spanish')
    filtered = [w for w in tkn_list if w not in stop_words]

    my_result = []
    for word in filtered:
        ls = ps.stem(word)
        myStr = ''.join(ls)
        my_result.append(myStr)
    return my_result


def idf(index, term):
    _, n_docs = index.shape
    df = np.count_nonzero(index.loc[term])
    return math.log(float(n_docs) / df)


def simple_dot_product(a, b):
    dsum = 0.
    for ((idx,), val) in np.ndenumerate(a):
        dsum += float(val) * float(b[idx])
    return dsum


def l2_norm(a): return math.sqrt(np.dot(a, a))


def cosine_similarity(a, b): return np.dot(a, b) / (l2_norm(a) * l2_norm(b))


def tfidf(tf, IDF): return tf * IDF


def query_vector(theIndex, query_terms):
    query_terms = set(query_terms)
    n_terms, _ = theIndex.shape
    query_vec = np.zeros(n_terms)

    for idx, term in enumerate(theIndex.index):
        if term in query_terms:
            query_vec[idx] = idf(theIndex, term)

    return query_vec


def query(index, query_terms):
    q = query_vector(index, query_terms)
    n_terms, _ = index.shape

    results = []
    for idoc in index:
        doc_vec = np.zeros(n_terms)

        for (idx, (term, tf)) in enumerate(index[idoc].iteritems()):
            doc_vec[idx] = tf * idf(index, term)

        results.append((idoc, cosine_similarity(q, doc_vec)))

    return sorted(results, key=lambda t: t[1], reverse=True)

# -----------------------------------------------END-OF-FUNCTIONS-------------------------------------------------------


# ----------------------------BEGIN-OF--PREPROCESSING-AND-SAVING-IN-VARIABLE-MYLIST-------------------------------------
file = open("test.json", "r")

myList = list()
for x in range(2):
    j = file.readline()
    doc = json.loads(j)
    s = list_stem_and_tokenize(doc['text'])
    list_stem_and_tokenized_words_in_the_documents = ' '.join(s)
    myList.append(list_stem_and_tokenized_words_in_the_documents)
    file.readline()
    file.readline()
file.close()
# ----------------------------END-OF--PREPROCESSING-AND-SAVING-IN-VARIABLE-MYLIST-------------------------------------

# -------------------------------------BEGIN-OF-BUILDING-INDEX-TABLE--------------------------------------------------
# uso la libreria sklearn
tfidf = TfidfVectorizer()

vectorsTfIdf = tfidf.fit_transform(myList)
feature_names = tfidf.get_feature_names()
feature_names_list = list(feature_names)
dense = vectorsTfIdf.todense()
denselist = dense.tolist()

# uso la libreria pandas
x = np.array(dense)
indexTable = pd.DataFrame(x, columns=feature_names)
transIndTable = indexTable.transpose()  # esta es la tabla de indices que siempre uso
# -------------------------------------END-OF-BUILDING-INDEX-TABLE--------------------------------------------------

# ---------------------------------------BEGIN-OF-PROGRAM-----------------------------------------------------
myQuery = str(input("Insert Query: "))
queryTerms = list_stem_and_tokenize(myQuery)

result = query(transIndTable, queryTerms)

for z in result:
    print(z)
# ---------------------------------------END-OF-PROGRAM-----------------------------------------------------
