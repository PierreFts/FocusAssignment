from flask import Flask, request, jsonify
import requests
import torch
from sentence_transformers import SentenceTransformer
import time


app = Flask(__name__)
model = None

@app.route('/', methods=['POST'])
def search():
    data = request.json  # Access the entire JSON payload
    headers = {'X-Request-Source': 'api'}
    url = 'http://model:5001/'
    response = requests.post(url, json=data, headers=headers)
    return {"vectors" : response.json()}



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
