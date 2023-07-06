from sentence_transformers import SentenceTransformer

if __name__ == '__main__':
    modelPath = "model_artifacts"
    model = SentenceTransformer(modelPath)
    sentences = ["This is a coding assignment", "We are in the first task."]
    embeddings = model.encode(sentences)

    #checking the embeddings
    shape = embeddings.shape
    if(shape[0]!=len(sentences)):
        print("problem : not one vector per input")
    else:
        print("no issue")