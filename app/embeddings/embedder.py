import json

import chromadb

from sentence_transformers import SentenceTransformer
from app.core.config import CHUNKS_FILE, CHROMA_DIR


# LOAD EMBEDDING MODEL
#change model if sys handles this one well
model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


# LOAD CHUNKS

with open(
    CHUNKS_FILE,
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)




client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="fastapi_docs"
)


# PREPARE DATA


documents = []
metadatas = []
ids = []


for chunk in chunks:

    code_text = "\n\n".join(
        [
            block["code"]
            for block in chunk["code_blocks"]
        ]
    )

    combined_text = f"""
Heading:
{chunk['heading']}

Content:
{chunk['content']}

Code Examples:
{code_text}
"""

    documents.append(combined_text)

    metadatas.append(
        {
            "heading": chunk["heading"],
            "level": chunk["level"],
            "source_file": chunk.get(
                "source_file",
                "unknown"
            ),
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