from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session, Response,jsonify
import json
import tf_idf


from datetime import datetime


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rankedRetrieval')
def rankedRetrieval():
    return render_template('ranked.html')

#retorna un json con los resultados
@app.route('/do_ranked_search/<query>', methods=['POST','GET'])
def get_ranked_results_by_query(query):
    results = []
    if len(query) > 0:

        token_list = tf_idf.stem_and_tokenize(query)
        query_vector = tf_idf.input_vector(token_list)
        tf_idf.tf_idf_query(query_vector)
        result = tf_idf.query_result(query_vector)
        f_result = result[:10]
        for element in f_result:
            record = {}
            record['name'] = str(element[0])
            record['weight'] =str(element[1])
            results.append(record)
            print("The DocID " + str(element[0]) + " matches, with weight " + str(element[1]))


    print(query)
    print(results)
    return jsonify(results)







if __name__ == '__main__':
    app.run(debug=True)
