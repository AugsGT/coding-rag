import json

from rank_bm25 import BM25Okapi

from app.core.config import (
    CHUNKS_FILE
)


# -----------------------------------
# LOAD CHUNKS
# -----------------------------------

with open(
    CHUNKS_FILE,
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)


# -----------------------------------
# PREPARE TEXT CORPUS
# -----------------------------------

documents = []

for chunk in chunks:

    code_text = "\n".join(
        [
            block["code"]
            for block in chunk["code_blocks"]
        ]
    )

    combined_text = f"""
    {chunk['heading']}
    {chunk['content']}
    {code_text}
    """

    documents.append(combined_text)


# -----------------------------------
# TOKENIZE
# -----------------------------------

tokenized_corpus = [
    doc.lower().split()
    for doc in documents
]


# -----------------------------------
# INIT BM25
# -----------------------------------

bm25 = BM25Okapi(
    tokenized_corpus
)


# -----------------------------------
# SEARCH
# -----------------------------------

def bm25_search(
    query,
    top_k=5
):

    tokenized_query = (
        query.lower().split()
    )

    scores = bm25.get_scores(
        tokenized_query
    )

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True,
    )[:top_k]

    results = []

    for idx in ranked_indices:

        results.append(
            {
                "score": float(scores[idx]),
                "chunk": chunks[idx],
            }
        )

    return results


# -----------------------------------
# TEST
# -----------------------------------

if __name__ == "__main__":

    query = input(
        "\nEnter query: "
    )

    results = bm25_search(query)

    print("\n" + "=" * 80)

    for i, result in enumerate(results):

        chunk = result["chunk"]

        print(f"\nRESULT {i+1}")
        print("-" * 80)

        print(
            f"Score: {result['score']:.4f}"
        )

        print(
            f"Heading: {chunk['heading']}"
        )

        print(
            f"Source: {chunk.get('source_file', 'unknown')}"
        )

        print("\nCONTENT:\n")

        print(chunk["content"][:1000])

        print("\n" + "=" * 80)