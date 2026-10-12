# IRForge

IRForge is a small information retrieval engine built from scratch for learning and experimentation

It turns a folder of text documents into a positional inverted index and supports Boolean AND searches and exact phrase searches

## What it demonstrates

- Tokenization and normalization
- Inverted index construction
- Positional postings
- Boolean AND query processing
- Phrase query processing

The project uses only the Python standard library in its first version

## Requirements

- Python 3.10 or newer

## Run the project

From the project folder create and activate a virtual environment if you want to keep the project dependencies isolated

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -e .
py -m irforge
```

On macOS or Linux use the matching activation command

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m irforge
```

## Try a few searches

```text
Search> database AND records
Boolean AND results: D1, D2, D3, D4

Search> "database stores"
Phrase results: D1, D3, D4

Search> "database records"
Phrase results: No matches
```

Use `:index` to inspect the terms and their positions

Use `:quit` to close the program

## Run the tests

```powershell
py -m unittest discover -s tests -v
```

## Project structure

```text
IRForge/
├── data/sample_docs/       Example text documents
├── src/irforge/            Search engine source code
├── tests/                  Tests for indexing and searching
└── pyproject.toml          Project configuration
```

## Planned improvements

1. Add OR and NOT Boolean operators
2. Add proximity queries such as `database /2 records`
3. Add SPIMI indexing with blocks and a merge step
4. Add a small search interface and compare indexing methods

## Learning notes

This project is intended to make the indexing and query processing steps visible

The current version uses a small in memory index and is not intended to compete with production search systems
