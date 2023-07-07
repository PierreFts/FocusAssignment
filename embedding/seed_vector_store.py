from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'])
print(es.ping())
# Check if the connection is successful
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Connection to Elasticsearch failed")


es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])


index_name = 'my_vectorspace'
index_mapping = {
    'properties': {
        'vector': {
            'type': 'dense_vector',
            'dims': 3  # Dimensionality of the vector
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

vectors = [
    {'vector': [0.1, 0.5, 0.8]},
    {'vector': [0.3, 0.7, 0.2]},
    {'vector': [0.6, 0.2, 0.9]}
]

def generate_documents():
    for i, vector in enumerate(vectors):
        yield {
            '_index': index_name,
            '_id': i + 1,
            '_source': vector
        }

bulk(es, generate_documents())


query_vector = [0.2, 0.4, 0.7]
k = 2



search_body = {
    'query': {
        'knn': {
            'vector': {
                'query_vector': query_vector,
                'field': 'vector',
                'k': k
            }
        }
    }
}



response = es.search(index=index_name, body=search_body)
results = response['hits']['hits']

for result in results:
    doc_id = result['_id']
    score = result['_score']
    print(f'Document ID: {doc_id}, Score: {score}')

