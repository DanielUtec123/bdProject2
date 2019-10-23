from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session, Response
import json


from datetime import datetime


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rankedRetrieval')
def rankedRetrieval():
    return render_template('ranked.html')

@app.route('/do_ranked_search/<query>', methods=['POST','GET'])
def get_ranked_results_by_query(query):
    query = request.form['query']
    return render_template("index.html")

@app.route('/raned/<sala_pin>', methods = ['GET'])
def get_message_by_pin(sala_pin):
    print(sala_pin)
    return render_template("index.html")







if __name__ == '__main__':
    app.run(debug=True)
