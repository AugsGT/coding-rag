from ollama import chat

from app.retrieval.search import (
    search_docs
)


SYSTEM_PROMPT = """
You are a coding documentation assistant.

Answer ONLY using the provided documentation context.

Rules:
- Do not hallucinate APIs or syntax
- Do not invent examples not present in context
- If answer is missing from context, say:
  "Insufficient documentation context."
- Prefer code examples when available
- Be concise and technical
- Cite SOURCE FILE and SECTION when relevant
"""


def build_context(results):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    context_parts = []

    for idx, doc in enumerate(documents):

        metadata = metadatas[idx]

        heading = metadata.get(
            "heading",
            "unknown"
        )

        source_file = metadata.get(
            "source_file",
            "unknown"
        )

        distance = distances[idx]

        context_parts.append(
            f"""
DOCUMENT {idx+1}

SOURCE FILE:
{source_file}

SECTION:
{heading}

SIMILARITY SCORE:
{distance:.4f}

CONTENT:
{doc}
"""
        )

    return "\n".join(context_parts)


def ask_rag(query):

    # -------------------------
    # RETRIEVE
    # -------------------------

    results = search_docs(query)

    context = build_context(results)

    # -------------------------
    # BUILD PROMPT
    # -------------------------

    user_prompt = f"""
Question:
{query}

Documentation Context:
{context}
"""

    # -------------------------
    # GENERATE
    # -------------------------

    response = chat(
        model="qwen2.5-coder:3b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return response["message"]["content"]


if __name__ == "__main__":

    while True:

        query = input(
            "\nAsk question: "
        )

        if query.lower() in [
            "exit",
            "quit"
        ]:
            break

        answer = ask_rag(query)

        print("\n" + "=" * 80)
        print(answer)
        print("=" * 80)