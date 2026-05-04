from pathlib import Path
from markdown_it import MarkdownIt


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

    i = 0

    while i < len(tokens):
        token = tokens[i]

        # -------------------------
        # HEADINGS
        # -------------------------
        if token.type == "heading_open":

            # Save previous section
            if current_section["content"] or current_section["code_blocks"]:
                sections.append(current_section)

            heading_level = int(token.tag[1])

            heading_text = ""

            # heading text is usually next token
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]

                if next_token.type == "inline":
                    heading_text = next_token.content

            current_section = {
                "heading": heading_text,
                "level": heading_level,
                "content": [],
                "code_blocks": [],
            }

        # -------------------------
        # PARAGRAPHS / TEXT
        # -------------------------
        elif token.type == "inline":
            current_section["content"].append(
                token.content
            )

        # -------------------------
        # CODE BLOCKS
        # -------------------------
        elif token.type == "fence":
            current_section["code_blocks"].append(
                {
                    "language": token.info,
                    "code": token.content,
                }
            )

        i += 1

    # append final section
    if current_section["content"] or current_section["code_blocks"]:
        sections.append(current_section)

    return sections


sections = extract_sections(tokens)

print(f"\nExtracted {len(sections)} sections\n")

for section in sections[:5]:

    print("=" * 60)

    print(f"Heading: {section['heading']}")
    print(f"Level: {section['level']}")

    print("\nCONTENT:")
    print("\n".join(section["content"][:3]))

    print("\nCODE BLOCKS:")
    print(len(section["code_blocks"]))