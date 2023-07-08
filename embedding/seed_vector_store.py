from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import requests
import json
import time

# Connect to Elasticsearch
# es = Elasticsearch(['http://localhost:9200'])
# Check if the connection is successful
# if es.ping():
#     print("Connected to Elasticsearch")
# else:
#     print("Connection to Elasticsearch failed")

dim_tot=768
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])


index_name = 'my_vectorspace'
index_mapping = {
    'properties': {
        'vector': {
            'type': 'dense_vector',
            'dims': dim_tot,  # Dimensionality of the vector, if test version just put 3 here
            'similarity': 'cosine',
            'index': True
        },
        'text': {
            'type': 'text'
        }
    }
}
if es.indices.exists(index=index_name):
    print("Index already exists")
    es.indices.delete(index=index_name)
    print("Index deleted")
else:
    print("Index does not exist")

es.indices.create(index=index_name, body={'mappings': index_mapping})

#let's check the mapping
# mapping = es.indices.get_mapping(index=index_name)
# print(mapping)


data = ["my first example", "I hope it works", "j'aime la baguette et le vin", "je construis des igloos"]
headers = {'X-Request-Source':'seed'}
url = 'http://localhost:5001/'
response = requests.post(url, json=data, headers=headers)
#response.json is a list of the vectors corresponding to data
embedded_vectors = response.json()

# Test version for dev, useful if issues

# vectors = [
#     {'vector': [0.1, 0.5, 0.8]},
#     {'vector': [0.3, 0.7, 0.2]},
#     {'vector': [0.6, 0.2, 0.9]}
# ]


# def generate_documents():
#     for i, vect in enumerate(vectors):
#         yield {
#             '_index': index_name,
#             '_id': i + 1,
#             '_source': {
#                 'vector': vect['vector'],
#                 'text': str(i)
#             }
#         }
# #query vector for the test version
# query_vector = [0.2, 1.0, 1.6]


def generate_documents2():
    for i, (vector, text) in enumerate(zip(embedded_vectors, data)):
        #print(f"Vector: {vector}, Text: {text}")
        yield {
            '_index': index_name,
            '_id': i+1,
            '_source': {
                'vector': vector,
                'text': text
            }
        }


bulk(es, generate_documents2())
time.sleep(1) #gives time to the store to update before we query it



#We check the number of elements in the vector store
# response = es.search(index=index_name, body={"query": {"match_all": {}}})
# hits = response["hits"]["hits"]
# print(f"Total Hits: {len(hits)}")
# for hit in hits:
#     print(hit)

k = 3

query_vector = requests.post(url, json="I hate my car", headers=headers).json()


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


for result in results:
    doc_id = result['_id']
    sentence = result['_source']['text']
    score = result['_score']
    print(f'Document ID: {doc_id}, Text: {sentence} Score: {score}')

