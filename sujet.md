# Assignment: Creating an end-to-end vector search API
_In this assignment you will showcase how to set up an end-to-end vector search API on your localhost. The main objective is to test your current performance on deploying ML/AI algorithms in a production-like setting. Very frequently Datascientists are not very experienced with deployments of such algorithms. Therefore, this assignment is intended to test your current state of this knowledge and/or your capabilities to learn fast. Roughly you will be (i) deploying an embedding model using a framework of choice, (ii) setting up vector store/database, (iii) create and deploy a very simple API to perform a kNN search with textual input._

**Some practical considerations when writing the case**:
1. We prefer that code is written in Python, because most of our backend is. If there are good reasons for using different languages, feel free to do so. It is not a hard requirement.
2. Make sure your code is well documented and good to read.
3. Make sure your instructions on how to use the code match the reality.
4. If, for some reason, you are not able to implement/code some of the components that are required; generate some fake responses/output such that you can continue with the other part, and are not stuck at one single subtask.

**Instructions**:
1. Create script called `build_model.py` which builds an embedding model transforming input text(s) into vector(s). You may create a custom model, or use a pretrained model. The actual performance of the model does not matter too much for this example. Make sure that the model artifacts will be stored in the `model_artifacts` folder.
2. Using `Docker` (and/or `docker-compose`), deploy the model stored in the `model_artifacts` folder, such that it can be served using `http` calls. You may use frameworks like `Tensorflow Serving` or `TorchServe` for this. This is likely dependent on your choice of framework in step 1.
3. Using `Docker` (and/or `docker-compose`), deploy a vector store like Elasticsearch, Pinecone, or Weaviate. Any other of your choice is also fine. There must be plenty of examples on the internet to do so.
4. Create script called `seed_vector_store.py`, which seeds the vector store with a couple of example records. You can generate/create the example records yourself. Make sure that the textual input is vectorized/embedded using API calls to the model deployed in 2. After running this script the vector store must be seeded with some examples.
5. Create a VERY basic API (e.g. use Flask or FastAPI or Django) with an endpoint that takes textual input, embeds the text into a vector and performs kNN search against the vectorstore. Return the record(s) found using kNN to the response of the endpoint. Please deploy this API on `Docker`.

**Expected outcome**
When all steps are succeeded you will have 3 services running; (i) the model (ii) the vector store, (iii) the API. By calling the API you will be able to search the nearest records for any given textual input.

If there is any questions, do not hesitate to contact me. I am happy to explain more.