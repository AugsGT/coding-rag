# Coding-RAG

Local-first Retrieval-Augmented Generation (RAG) system for programming documentation.

This project ingests markdown documentation, cleans and chunks the corpus, generates semantic embeddings, stores vectors locally in ChromaDB, and uses Ollama for grounded answer generation.

---

# Features

* Markdown documentation ingestion
* Recursive multi-file corpus parsing
* HTML/noise filtering
* Semantic chunking pipeline
* Local embedding generation
* ChromaDB vector storage
* Semantic retrieval
* Ollama-powered grounded generation
* Source-aware retrieval metadata
* Local-first architecture
* No paid APIs required

---

# Current Architecture

```text
Markdown Docs
    ↓
Parser
    ↓
Cleaning + Filtering
    ↓
Semantic Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Retriever
    ↓
Ollama
    ↓
Grounded Response
```

---

# Tech Stack

## Core

* Python 3.12+
* uv
* Git

## Retrieval

* ChromaDB
* sentence-transformers
* BAAI/bge-small-en-v1.5

## LLM

* Ollama
* qwen2.5-coder:3b

## Parsing

* markdown-it-py

---

# Project Structure

```text
coding-rag/
│
├── app/
│   ├── chunking/
│   │   └── chunker.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── ingestion/
│   │   ├── filter.py
│   │   └── parser.py
│   │
│   ├── llm/
│   │   └── rag.py
│   │
│   └── retrieval/
│       └── search.py
│
├── data/
│   ├── chroma/
│   ├── processed/
│   └── raw/
│
├── .gitignore
├── pyproject.toml
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repo-url>
cd coding-rag
```

---

## Install uv

Windows:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Create Virtual Environment

```powershell
uv venv
```

Activate:

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```powershell
uv sync
```

Or manually:

```powershell
uv add chromadb sentence-transformers markdown-it-py ollama
```

---

# Ollama Setup

Install Ollama:

[https://ollama.com/download/windows](https://ollama.com/download/windows)

Pull model:

```powershell
ollama pull qwen2.5-coder:3b
```

---

# Documentation Corpus Setup

Clone documentation repositories into:

```text
data/raw/
```

Example:

```powershell
git clone https://github.com/fastapi/fastapi.git data/raw/fastapi
```

---

# Pipeline

## 1. Parse Documentation

```powershell
python -m app.ingestion.parser
```

---

## 2. Generate Chunks

```powershell
python -m app.chunking.chunker
```

---

## 3. Generate Embeddings

```powershell
python -m app.embeddings.embedder
```

---

## 4. Run Semantic Search

```powershell
python -m app.retrieval.search
```

---

## 5. Run RAG System

```powershell
python -m app.llm.rag
```

---

# Example Query

```text
Ask question: how to create async routes
```

Example response:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}
```

---

# Current Limitations

* Retrieval ambiguity for semantically similar concepts
* Chunking still section-oriented
* No reranker yet
* No hybrid BM25 retrieval yet
* Context compression not implemented
* No evaluation benchmark harness yet

---

# Planned Improvements

* Hybrid BM25 + vector retrieval
* Cross-encoder reranking
* Better concept-level chunking
* Source citations in answers
* Retrieval evaluation suite
* FastAPI API layer
* Web UI
* Repository-aware RAG
* AST/code-aware retrieval

---

# Why This Project Exists

Most beginner RAG projects:

* skip ingestion quality
* use raw file embeddings
* rely heavily on frameworks
* ignore retrieval debugging

This project focuses on:

* retrieval engineering
* corpus quality
* local-first inference
* transparent architecture
* debuggable pipelines

---

# Notes

This project is designed as an educational and engineering-focused RAG system.

The goal is to understand:

* ingestion pipelines
* chunking strategies
* semantic retrieval
* grounded generation
* retrieval failure modes

instead of only building a chatbot wrapper.

---

# License

MIT
