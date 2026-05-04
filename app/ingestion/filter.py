import re


BAD_HEADINGS = {
    "Silver Sponsors",
    "FastAPI Conf",
    "FastAPI mini documentary",
}


def clean_text(text: str) -> str:
    """
    Clean extracted markdown text.
    """

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove markdown anchors
    text = re.sub(r"\s*{#.*?}", "", text)

    # Remove markdown links
    # [text](url) -> text
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_useful_section(section: dict) -> bool:
    """
    Decide whether a section is useful for retrieval.
    """

    heading = section["heading"].strip()

    # Remove useless headings
    if heading in BAD_HEADINGS:
        return False

    # Remove empty sections
    if (
        not section["content"]
        and not section["code_blocks"]
    ):
        return False

    # Remove image/banner-heavy junk
    combined_text = " ".join(section["content"])

    junk_patterns = [
        "img src=",
        "youtube.com",
        "sponsors",
        "documentary",
    ]

    combined_text_lower = combined_text.lower()

    for pattern in junk_patterns:

        if pattern in combined_text_lower:
            return False

    return True


def clean_section(section: dict) -> dict:
    """
    Clean an entire section.
    """

    cleaned_content = []

    for text in section["content"]:

        cleaned = clean_text(text)

        if cleaned:
            cleaned_content.append(cleaned)

    cleaned_code_blocks = []

    for block in section["code_blocks"]:

        code = block["code"].strip()

        if code:

            cleaned_code_blocks.append(
                {
                    "language": block["language"],
                    "code": code,
                }
            )

    return {
        "heading": clean_text(section["heading"]),
        "level": section["level"],
        "content": cleaned_content,
        "code_blocks": cleaned_code_blocks,
    }