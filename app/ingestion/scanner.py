from pathlib import Path

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
        r"C:\Storage\docs-corpus\fastapi\docs\en\docs"
    )

    print(f"Found {len(files)} markdown files")

    for f in files[:10]:
        print(f)