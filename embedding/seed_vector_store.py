from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import requests
import json
import time



dim_tot=768 #dimension of the embedded space
# Here we define our vector space with its name and its attributes. The text attribute will be used to store the sentence corresponding to the vector.
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




if __name__ == '__main__':


    # We connect to the store. It is interesting to note that it's the only point in our application where we use "localhost" since all the other service refer
    # to each other with their names, defined in the docker-compose.yml file. Here since we are not in their network, we can't and we have to use localhost.
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])


    # We really want the vector store to be what we just defined, so if a vectorspace with the same name already exists, we will delete it to take its place with 
    # the attributes we want.
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

    # We now define the elements we want to seed in our vector store. Feel free to add or remove strings in that list.
    data = ["my first example", "I hope it works", "j'aime la baguette et le vin", "je construis des igloos"]
    headers = {'X-Request-Source':'seed'}
    url = 'http://localhost:5001/'

    # Here we translate the sentences into vectors thanks to the dedicated service.
    response = requests.post(url, json=data, headers=headers)

    #response.json is a list of the vectors corresponding to data
    embedded_vectors = response.json()



    # This function generates the document that corresponds to our vector so that we can give it to our vector store.
    def generate_documents():
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

    # Now we send the document to our vectore store.
    bulk(es, generate_documents())
    time.sleep(1) #gives time to the store to update before we query it


    ############################################# You can ignore this part
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
    #############################################

    ###################################################################### You can ignore this part
    #We check the number of elements in the vector store
    # response = es.search(index=index_name, body={"query": {"match_all": {}}})
    # hits = response["hits"]["hits"]
    # print(f"Total Hits: {len(hits)}")
    # for hit in hits:
    #     print(hit)
    #further prints to see the embeddings, from the doc of hugging face
    # for sentence, embedding in zip(sentences, embeddings):
    #     print("Sentence:", sentence)
    #     print("Embedding:", embedding)
    #     print("")
    ######################################################################