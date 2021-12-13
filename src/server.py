import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import json
from deconstructor import mapComponent
import re

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = False

def preprocess(comp, text):
    if comp != "Rhyme Scheme":
        sentences = list(map(lambda x: x.strip(),re.split(";|\.|\n", text)))
        # print(sentences)
        # What is the delimiter??
    else:
        sentences = list(filter(lambda x: x,map(lambda x: x.strip(),text.split("\n"))))
    if len(sentences[-1]) == 0:
        return sentences[:-1]
    else:
        # print(len(sentences[-1]))
        return sentences

@app.route('/', methods=['GET'])
def home():
    return "<h1>Sentence Deconstructor</h1><p>Capstone Project 2021</p>"

@cross_origin()
@app.route('/deconstructor', methods = ['POST'])
def deconstruct():
    print(request.method)
    comp = request.json['component']
    text = request.json['text'].strip()
    paragraph = 1

    processed_text = preprocess(comp, text) # List of sentences
    print("Processed Text: ", processed_text)
    # return "Done"
    # The input passed to each class while instantiating is a LIST of sentences 
    obj = mapComponent[comp](processed_text, paragraph) # Mapping the component requested to appropriate class and instantiating object
    result = obj.execute()

    return jsonify(result)
        
    # return jsonify(mapComponent)

# app.run(host="0.0.0.0")
app.run()