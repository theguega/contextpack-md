# contextpack

An open-source tool to extract high-quality context from websites and documentation for LLMs.

## Features

- **Query Documentation**: Crawl and extract content from documentation pages recursively.
- **Ask Web**: Search the web and gather relevant context chunks ranked by similarity.
- **Repository Ingestion**: Ingest code repositories natively. Respects `.gitignore` and ignores lock files/binaries.
- **LLM-Ready**: Outputs clean markdown optimized for LLM prompts.
- **Library-First**: Can be used as a CLI tool or a Python library.
- **Stateless & Portable**: Works as a standalone tool or a microservice component.

## Installation

This project uses Pixi and uv for dependency management.

```bash
uv sync
```

## CLI Usage

### Query Documentation
Extract documentation context starting from a given page. You can control the recursion depth and maximum pages.

```bash
# Query only this page (depth 0)
uv run contextpack query https://docs.ros.org/en/humble/Concepts.html --depth 0

# Full documentation crawl (default depth 2)
uv run contextpack query https://docs.ros.org/en/humble/Concepts.html --depth 2 --max-pages 20
```

### Ask the Web
Automatically gather relevant context from the web for a question. It uses DuckDuckGo to find sources and ranks content chunks by relevance.

```bash
uv run contextpack ask "how ros2 qos works"
```

### Ingest Repository
Clone and ingest a GitHub repository to extract text-based files. Automatically skips binary files, huge assets, and lock files, strictly respecting `.gitignore` rules.

```bash
uv run contextpack repo https://github.com/tiangolo/typer.git
```

## Python Library Usage

The library is designed to be easily integrated into AI agents or pipelines.

```python
from contextpack import query_url, ask_web

# Query documentation with custom depth
result = query_url(
    "https://docs.ros.org/en/humble/Concepts.html", 
    max_depth=0, 
    max_pages=1
)
print(result.context)

# Ask the web
result = ask_web("how ros2 qos works")
print(result.context)

# Ingest a repository
from contextpack import ingest_repo
repo_result = ingest_repo("https://github.com/tiangolo/typer.git")
print(repo_result.context)
```

## Architecture

The project follows a library-first architecture:
- `api.py`: Core orchestration API.
- `repo.py`: GitHub repository ingestion module.
- `crawler.py`: Recursive documentation crawler (domain-constrained).
- `scraper.py`: Content extraction using `trafilatura`.
- `chunker.py`: Paragraph-aware text splitting.
- `embeddings.py`: `sentence-transformers` integration (Lazy-loaded).
- `ranker.py`: Cosine similarity ranking.
- `formatter.py`: LLM-optimized Markdown formatting.
- `cli.py`: `Typer` CLI wrapper.

## Performance Constraints

- **Max pages per run**: 10 (default), configurable via CLI.
- **Crawl depth**: 2 (default), configurable via CLI.
- **Request timeout**: 10 seconds.
- **Content limit**: Skips pages larger than 1MB.
- **Duplicates**: Automatically skips duplicate URLs within the same run.
