import re


def clean_text(text: str) -> str:

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove markdown anchors
    text = re.sub(r"\s*\{#.*?\}", "", text)

    # Remove image placeholders
    text = re.sub(r"!\S+", "", text)

    return text.strip()