from flask import Flask, request, jsonify
import requests
import torch
from sentence_transformers import SentenceTransformer
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

app = Flask(__name__)
index_name = 'my_vectorspace'
k = 3 #number of closest vectors we want to return



@app.route('/', methods=['POST'])
def search():
    data = request.json  # Access the entire JSON payload

    #we get the embedded vector 
    headers = {'X-Request-Source': 'api'}
    url = 'http://model:5001/'
    response = requests.post(url, json=data, headers=headers)
    query_vector = response.json()[0] #[0] is mandatory here since the vector is inside a list (it's the list's only element) and the search needs the vector itself


    #we connect to the store
    es = Elasticsearch([{'host': 'store', 'port': 9200, 'scheme': 'http'}])

    #we build the query "knn" in the store, send it, stock the results
    search_body = {
            'knn': {
                'query_vector': query_vector,
                'field': 'vector',
                'k': k ,
                'num_candidates' : 100
            },
            "fields": ["text"]
        }
    response = es.search(index=index_name, body=search_body)
    results = response['hits']['hits']


    return({"results" : results}) #Having a dictionary is critical for sending the info through the return to the api end


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
