# FocusAssignment

In this assignment, I have set up an end-to-end vector search API on my localhost. It works with docker-compose, flask, requests, faker and the hugging face sentence-transformer library so be careful and check that you have them on your machine. You can for instance install the hugging face sentence-transformer library with pip: "pip install -U sentence-transformers".
The whole project is coded in python and runs locally.

**Architecture**:

The general architecture when working is as follows: we have three services running with dicker-compose : api, store and model. When we send a request, it is sent to api which then uses the model service to transform our request into a vector, and then api sends a query to the store service to compare this vector with what is already in the store. 

**Instructions**:

Once you have cloned the repository locally, you can start the application. Here are the steps: 
1. First, we have to build the model itself before it can be loaded in the model service. To do so, execute the script `build_model.py`. If everything went well, you can now see a new `model_artifacts` folder inside the `service_model`S folder. The algorithm we will use to transform the sentences into embedded vectors is `AI-Growth-Lab/PatentSBERTa`.
2. Then, we can start our docker compose. This step can take quite some time depending on several factors such as your internet connection since we will download a docker image and we will also build two of them. A drawback here is that the images we build are quite big (11-12GB). It's a minor problem which could be addressed in the future. To start the services, go to the `embedding` folder and type `docker-compose up`. Wait until the services are up and running.
3. Now that the services are up and running, we can seed the vector store. to do so, just execute the script `seed_vector_store.py`. It shouldn't take too long.
4. Now you can easily send requests to the application by starting the script `make_req.py`. It will ask you to write the sentence you want to use as an input and will perform the knn algorithm as wanted before sending back the closest elements with their associated score.

**Remarks**: 

1. The big drawbacks of this application is that the built images are heavy, this is a first version and this point could totally be addressed in the future.
2. The vectors we put in the store correspond to sentences that are hard-coded in the script `seed_vector_store.py` (to be able to add sentences we would like to be there) and a set of randomly generated sentences. This is not the cleanest way possible but it is very useful to demonstrate that the whole system is working while being able to easily manage the number of elements in the store. The drawback is that most of the sentence are not real ones but once again, it could be addressed in the future with no problem.
3. Since we run all the services locally and with the goal to show the working services, some points would have to be modified to be better addapted for bigger scale, for ecample the number of notes we run on or the fact that we use simple http protocols instead of https. We didn't work on security concerns and this should be addressed before any real launch.