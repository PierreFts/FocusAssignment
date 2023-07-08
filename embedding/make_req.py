
import requests
import json


url = "http://localhost:5002/" # for docker, the api address


if __name__ == '__main__':

    #we create the data we want to use to enquire the vector store
    query = input("Enter yout query: ")
    data = [query]
    j_data = json.dumps(data)

    #we send out request to the API
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=j_data, headers=headers).json()

    #we collect the results and print them in an easy to read way
    results = r["results"]
    print("Ranked closest neighbours in the vector store :")
    for result in results:
        doc_id = result['_id']
        sentence = result['_source']['text']
        score = result['_score']
        print(f'Document ID: {doc_id}, Text: {sentence} Score: {score}')