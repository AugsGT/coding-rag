from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Data subdirectories
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CHROMA_DIR = DATA_DIR / "chroma"

# Specific file paths
SECTIONS_FILE = PROCESSED_DATA_DIR / "sections.json"
CHUNKS_FILE = PROCESSED_DATA_DIR / "chunks.json"

# Default paths for ingestion
DEFAULT_CORPUS_DIR = RAW_DATA_DIR
DEFAULT_MARKDOWN_FILE = RAW_DATA_DIR / "index.md"
