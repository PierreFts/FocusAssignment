from sentence_transformers import SentenceTransformer
from flask import Flask, request, jsonify

from flask import Flask, jsonify
import requests

import os

app = Flask(__name__)


modelPath = "./model_artifacts"
# modelPath = "../model_artifacts"
model = SentenceTransformer(modelPath)

# @app.route('/')
# def index():
#     # Sending an HTTP request to service2
#     response = requests.get('http://service2:8000/process/42')
#     result = response.json()

#     # Sending an HTTP request to service3
#     response = requests.post('http://service3:9000/results', json=result)
#     return 'Result sent to service3'


@app.route('/', methods=['GET', 'POST'])
def transfo():
    if request.method=="POST":
        #custom header to know the origin of the request
        request_source = request.headers.get('X-Request-Source')
        data = request.get_json()
        print("data ---- > ", data)
        if request_source in ["api","seed"]:
            
            results = model.encode(data)
            return jsonify(results.tolist())
        elif request_source=="vect_space":
            return()
        else:
            #return("error in the request source")
            return(request_source)
    return "Not a proper request method or data"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

    # sentences = ["This is a coding assignment", "We are in the first task."]
    # embeddings = model.encode(sentences)