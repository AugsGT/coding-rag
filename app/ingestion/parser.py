from pathlib import Path
from markdown_it import MarkdownIt
import json
from app.core.config import SECTIONS_FILE
from app.ingestion.filter import (
    clean_text,
    clean_section,
    is_useful_section,
)


# DOCS ROOT

DOCS_PATH = Path(
    r"C:\Storage\docs-corpus\fastapi\docs\en\docs"
)

SUPPORTED_EXTENSIONS = {
    ".md",
    ".mdx",
}


# MARKDOWN PARSER

md = MarkdownIt()


# FILE SCANNER

def scan_markdown_files(root_path):

    files = []

    for file in root_path.rglob("*"):

        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(file)

    return files


# SECTION EXTRACTION

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
                    heading = clean_text(
                        next_token.content
                    )

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

                if cleaned and len(cleaned) > 3:

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


# INGEST FILES

all_sections = []

markdown_files = scan_markdown_files(
    DOCS_PATH
)

print(
    f"\nFound {len(markdown_files)} markdown files"
)

for file_path in markdown_files:

    try:

        markdown_text = file_path.read_text(
            encoding="utf-8"
        )

        tokens = md.parse(markdown_text)

        sections = extract_sections(tokens)

        for section in sections:

            cleaned = clean_section(
                section
            )

            if is_useful_section(cleaned):

                cleaned["source_file"] = str(
                    file_path.relative_to(
                        DOCS_PATH
                    )
                )

                all_sections.append(cleaned)

    except Exception as e:

        print(
            f"\nFailed parsing {file_path}"
        )

        print(e)


# SAVE OUTPUT

SECTIONS_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    SECTIONS_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_sections,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"\nSaved {len(all_sections)} sections"
)

print(
    f"\nSections saved to:"
)

print(SECTIONS_FILE)