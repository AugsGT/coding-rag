from ollama import chat

from app.retrieval.hybrid_search import (
    hybrid_search
)

SYSTEM_PROMPT = """
You are a coding documentation assistant.

Answer ONLY using the provided documentation context.

STRICT RULES:
- Never invent APIs, imports, syntax, or examples
- Never add external knowledge
- Only use information explicitly present in context
- If information is incomplete, say:
  "Insufficient documentation context."
- Prefer directly retrieved code examples
- Keep answers concise and technical
- Cite SOURCE FILE and SECTION when relevant
"""

def build_context(results):

    context_parts = []

    for idx, result in enumerate(results):

        heading = result.get(
            "heading",
            "unknown"
        )

        source_file = result.get(
            "source_file",
            "unknown"
        )

        score = result.get(
            "score",
            0.0
        )

        content = result.get(
            "content",
            ""
        )

        context_parts.append(
            f"""
DOCUMENT {idx+1}

SOURCE FILE:
{source_file}

SECTION:
{heading}

RETRIEVAL SCORE:
{score:.4f}

CONTENT:
{content}
"""
        )

    return "\n".join(context_parts)
def ask_rag(query):

    # -------------------------
    # RETRIEVE
    # -------------------------

    results = hybrid_search(
        query,
        top_k=2
    )
    context = build_context(results)
    print("\nRETRIEVED SOURCES:\n")

    for result in results:

        print(
            f"- {result['heading']} "
            f"({result['source_file']})"
        )

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