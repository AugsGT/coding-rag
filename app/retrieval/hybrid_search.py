from collections import defaultdict

from app.retrieval.search import (
    search_docs
)

from app.retrieval.bm25_search import (
    bm25_search
)



# HYBRID SEARCH

def hybrid_search(
    query,
    top_k=5,
    vector_weight=0.7,
    bm25_weight=0.3,
):


    # VECTOR SEARCH

    vector_results = search_docs(
        query,
        top_k=top_k
    )


    # BM25 SEARCH

    bm25_results = bm25_search(
        query,
        top_k=top_k
    )

    # SCORE MERGING
    merged_scores = defaultdict(float)

    merged_chunks = {}

    # VECTOR RESULTS

    vector_docs = vector_results[
        "documents"
    ][0]

    vector_meta = vector_results[
        "metadatas"
    ][0]

    vector_distances = vector_results[
        "distances"
    ][0]

    for idx, doc in enumerate(
        vector_docs
    ):

        metadata = vector_meta[idx]

        heading = metadata.get(
            "heading",
            "unknown"
        )

        source_file = metadata.get(
            "source_file",
            "unknown"
        )

        chunk_key = (
            heading,
            source_file
        )

        # Lower distance = better
        similarity_score = (
            1 / (
                vector_distances[idx]
                + 1e-6
            )
        )

        merged_scores[
            chunk_key
        ] += (
            similarity_score
            * vector_weight
        )

        merged_chunks[
            chunk_key
        ] = {
            "heading": heading,
            "source_file": source_file,
            "content": doc,
        }

    # BM25 RESULTS

    for result in bm25_results:

        chunk = result["chunk"]

        heading = chunk["heading"]

        source_file = chunk.get(
            "source_file",
            "unknown"
        )

        chunk_key = (
            heading,
            source_file
        )

        bm25_score = result["score"]

        merged_scores[
            chunk_key
        ] += (
            bm25_score
            * bm25_weight
        )

        if chunk_key not in merged_chunks:

            merged_chunks[
                chunk_key
            ] = {
                "heading": heading,
                "source_file": source_file,
                "content": chunk[
                    "content"
                ],
            }


    # SORT RESULTS

    ranked_results = sorted(
        merged_scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    final_results = []

    for (
        chunk_key,
        score
    ) in ranked_results[:top_k]:

        chunk_data = merged_chunks[
            chunk_key
        ]

        final_results.append(
            {
                "score": score,
                "heading": chunk_data[
                    "heading"
                ],
                "source_file": chunk_data[
                    "source_file"
                ],
                "content": chunk_data[
                    "content"
                ],
            }
        )

    return final_results



# TEST

if __name__ == "__main__":

    query = input(
        "\nEnter query: "
    )

    results = hybrid_search(query)

    print("\n" + "=" * 80)

    for i, result in enumerate(
        results
    ):

        print(f"\nRESULT {i+1}")
        print("-" * 80)

        print(
            f"Score: {result['score']:.4f}"
        )

        print(
            f"Heading: {result['heading']}"
        )

        print(
            f"Source: {result['source_file']}"
        )

        print("\nCONTENT:\n")

        print(
            result["content"][:1000]
        )

        print("\n" + "=" * 80)