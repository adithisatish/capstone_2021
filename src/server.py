import flask
from flask import request, jsonify
from deconstructor import mapComponent

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/deconstructor', methods=['POST'])
def deconstruct():
    return jsonify(mapComponent)

app.run()