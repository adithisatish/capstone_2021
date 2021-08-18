import flask
from flask import request, jsonify
import json
from deconstructor import mapComponent

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def preprocess(comp, text):
    if comp != "Rhyme Scheme":
        sentences = text.split(".")
        # print(sentences)
    else:
        sentences = []
    if len(sentences[-1]) == 0:
        return sentences[:-1]
    else:
        # print(len(sentences[-1]))
        return sentences

@app.route('/', methods=['GET'])
def home():
    return "<h1>Sentence Deconstructor</h1><p>Capstone Project 2021</p>"

@app.route('/deconstructor', methods=['POST'])
def deconstruct():
    comp = request.json['component']
    text = request.json['text']
    paragraph = 1

    processed_text = preprocess(comp, text)
    print("Processed Text: ", processed_text)
    # return "Done"
    obj = mapComponent[comp](processed_text, paragraph)
    result = obj.execute()

    return jsonify(result)
        
    # return jsonify(mapComponent)

app.run()