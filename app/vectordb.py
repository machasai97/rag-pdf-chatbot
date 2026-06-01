import chromadb


client = chromadb.Client()


collection = client.get_or_create_collection(
    name="pdf_collection"
)


def store_embeddings(chunks, embeddings):

    ids = []

    for index in range(len(chunks)):

        ids.append(str(index))


    collection.add(

        documents=chunks,

        embeddings=embeddings.tolist(),

        ids=ids
    )

    print("Stored Successfully")

    print(
        "Total Documents:",
        collection.count()
    )



def search_embeddings(query_embedding):

    results = collection.query(

        query_embeddings=[
            query_embedding.tolist()
        ],

        n_results=1
    )

    return results