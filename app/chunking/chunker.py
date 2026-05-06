import json
import uuid
from app.core.config import SECTIONS_FILE, CHUNKS_FILE
from app.ingestion.filter import clean_text

MAX_CHARS = 1500


def estimate_tokens(text: str) -> int:
    """
    Rough token estimation.
    """
    return len(text.split())


def split_large_text(text: str, max_chars: int):
    """
    Split large text into smaller chunks.
    Splits by paragraphs first.
    """

    paragraphs = text.split("\n")

    chunks = []

    current = ""

    for para in paragraphs:

        para = para.strip()

        if not para:
            continue

        # If adding paragraph exceeds limit
        if len(current) + len(para) > max_chars:

            if current:
                chunks.append(current.strip())

            current = para

        else:
            current += "\n" + para

    if current:
        chunks.append(current.strip())

    return chunks


def create_chunks(sections):

    chunks = []

    for section in sections:

        heading = clean_text(
    section["heading"]
)

        content_text = "\n".join(
            section["content"]
        )

        code_blocks = section["code_blocks"]

 
# SMALL SECTION
        
        if len(content_text) <= MAX_CHARS:

            chunk = {
                "chunk_id": str(uuid.uuid4()),
                "heading": heading,
                "level": section["level"],
                "content": content_text,
                "code_blocks": code_blocks,
                "tokens_estimate": estimate_tokens(
                    content_text
                ),
            }

            chunks.append(chunk)

      
        # LARGE SECTION
        else:

            split_chunks = split_large_text(
                content_text,
                MAX_CHARS
            )

            for idx, split_text in enumerate(
                split_chunks
            ):

                chunk = {
                    "chunk_id": str(uuid.uuid4()),
                    "heading": f"{heading} (part {idx+1})",
                    "level": section["level"],
                    "content": split_text,
                    "code_blocks": code_blocks,
                    "tokens_estimate": estimate_tokens(
                        split_text
                    ),
                }

                chunks.append(chunk)

    return chunks


if __name__ == "__main__":

    with open(
        SECTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        sections = json.load(f)

    chunks = create_chunks(sections)

    CHUNKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(
        CHUNKS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"\nCreated {len(chunks)} chunks")