from sentence_transformers import SentenceTransformer
from flask import Flask, request, jsonify
from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

modelPath = "./model_artifacts"
model = SentenceTransformer(modelPath)

@app.route('/', methods=['GET', 'POST'])
def transfo():
    if request.method=="POST":
        #custom header to know the origin of the request, not mandatory but a check for debugging.
        request_source = request.headers.get('X-Request-Source')

        data = request.get_json()
        print("data ---- > ", data) # more for debugging, will print the list of sentences we will transform in vectors.

        if request_source in ["api","seed"]: #source checking, to be sure we don't have strange enquires. More for debugging
            results = model.encode(data)
            return jsonify(results.tolist())

        else:
            return("error in the request source")

    return "Not a proper request method or data"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
