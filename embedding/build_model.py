from sentence_transformers import SentenceTransformer

if __name__ == '__main__':

    #file for artifacts
    model_artifacts_folder = "./service_model/model_artifacts"

    #the sentences we would like to encode, for tests
    sentences = ["This is a coding assignment", "We are in the first task."]

    #choice of our model, here we took a sentence transformer to have a vector per input sentence instead of one vector per token (so more than one per word...)
    model = SentenceTransformer('AI-Growth-Lab/PatentSBERTa')

    #its artifacts
    model.save(model_artifacts_folder)
    #tf.saved_model.save(model, model_artifacts_folder)

    #Sentences are encoded by calling model.encode()
    embeddings = model.encode(sentences)

    #checking the embeddings
    shape = embeddings.shape
    if(shape[0]!=len(sentences)):
        print("problem : not one vector per input")
    else:
        print("no issue")

    # #further prints to see the embeddings, from the doc of hugging face
    # for sentence, embedding in zip(sentences, embeddings):
    #     print("Sentence:", sentence)
    #     print("Embedding:", embedding)
    #     print("")