from pathlib import Path

from app.core.config import DEFAULT_CORPUS_DIR

SUPPORTED_EXTENSIONS = {".md", ".mdx"}

def scan_markdown_files(root_path: str):
    root = Path(root_path)

    files = []

    for file in root.rglob("*"):
        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(file)

    return files


if __name__ == "__main__":
    files = scan_markdown_files(
        DEFAULT_CORPUS_DIR
    )

    print(f"Found {len(files)} markdown files")

    for f in files[:10]:
        print(f)