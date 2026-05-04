from pathlib import Path
from markdown_it import MarkdownIt
import json

from cleaner import clean_text
from filter import (
    clean_text,
    clean_section,
    is_useful_section,
)

MARKDOWN_FILE = Path(
    r"C:\Storage\docs-corpus\fastapi\docs\en\docs\index.md"
)

markdown_text = MARKDOWN_FILE.read_text(
    encoding="utf-8"
)

md = MarkdownIt()

tokens = md.parse(markdown_text)


def extract_sections(tokens):

    sections = []

    current_section = {
        "heading": "ROOT",
        "level": 0,
        "content": [],
        "code_blocks": [],
    }

    inside_paragraph = False
    inside_list = False

    i = 0

    while i < len(tokens):

        token = tokens[i]

        # HEADINGS
        if token.type == "heading_open":

            if current_section["content"] or current_section["code_blocks"]:
                sections.append(current_section)

            level = int(token.tag[1])

            heading = ""

            if i + 1 < len(tokens):

                next_token = tokens[i + 1]

                if next_token.type == "inline":
                    heading = clean_text(next_token.content)

            current_section = {
                "heading": heading,
                "level": level,
                "content": [],
                "code_blocks": [],
            }

        # PARAGRAPHS
        elif token.type == "paragraph_open":
            inside_paragraph = True

        elif token.type == "paragraph_close":
            inside_paragraph = False

        # LISTS
        elif token.type in [
            "bullet_list_open",
            "ordered_list_open"
        ]:
            inside_list = True

        elif token.type in [
            "bullet_list_close",
            "ordered_list_close"
        ]:
            inside_list = False

        # CONTENT
        elif token.type == "inline":

            if inside_paragraph or inside_list:

                cleaned = clean_text(
                    token.content
                )

                if cleaned:
                    current_section["content"].append(
                        cleaned
                    )

        # CODE BLOCKS
        elif token.type == "fence":

            current_section["code_blocks"].append(
                {
                    "language": token.info.strip(),
                    "code": token.content.strip(),
                }
            )

        i += 1

    if current_section["content"] or current_section["code_blocks"]:
        sections.append(current_section)

    return sections


######################
#extracting sec
sections = extract_sections(tokens)


#############
#cleaning

cleaned_sections = []

for section in sections:

    cleaned = clean_section(section)

    if is_useful_section(cleaned):
        cleaned_sections.append(cleaned)

########################
#saving jsonm
with open(
    "sections.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        cleaned_sections,
        f,
        indent=2,
        ensure_ascii=False
    )


print(f"\nSaved {len(cleaned_sections)} sections")

