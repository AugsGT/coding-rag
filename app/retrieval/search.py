import chromadb

from sentence_transformers import (
    SentenceTransformer
)
from app.core.config import CHROMA_DIR


#model loading

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


#chroma conn

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="fastapi_docs"
)

#search

def search_docs(query, top_k=5):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results


#test

if __name__ == "__main__":

    query = input(
        "\nEnter query: "
    )

    results = search_docs(query)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n" + "=" * 80)

    for i in range(len(documents)):

        print(f"\nRESULT {i+1}")
        print("-" * 80)

        print(
            f"Heading: {metadatas[i]['heading']}"
        )

        print(
            f"Distance: {distances[i]:.4f}"
        )

        print("\nCONTENT:\n")

        print(documents[i][:1000])

        print("\n" + "=" * 80)