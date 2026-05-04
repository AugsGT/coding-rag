import json

import chromadb

from sentence_transformers import SentenceTransformer


# LOAD EMBEDDING MODEL
#change model if sys handles this one well
model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


# LOAD CHUNKS

with open(
    "../chunking/chunks.json",
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)




client = chromadb.PersistentClient(
    path="../../data/chroma"
)

collection = client.get_or_create_collection(
    name="fastapi_docs"
)


# PREPARE DATA


documents = []
metadatas = []
ids = []


for chunk in chunks:

    combined_text = f"""
Heading:
{chunk['heading']}

Content:
{chunk['content']}
"""

    documents.append(combined_text)

    metadatas.append(
        {
            "heading": chunk["heading"],
            "level": chunk["level"],
        }
    )

    ids.append(chunk["chunk_id"])


# GENERATE EMBEDDINGS

embeddings = model.encode(
    documents,
    show_progress_bar=True
)


# STORE IN CHROMA

collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings.tolist()
)

print(
    f"\nStored {len(documents)} chunks in ChromaDB"
)