# contextpack

A dead-simple tool to extract high-quality Markdown from any URL for LLMs.

## Features

- **Single Purpose**: Get clean, LLM-ready Markdown from a URL.
- **PDF Support**: Convert online PDFs to high-quality Markdown using `marker-pdf`.
- **Optional Local Storage**: Save results to a `.contextpack` folder.
- **Zero Configuration**: No complex ranking, crawling, or embedding setups.

## Installation

This project uses Pixi and uv for dependency management.

```bash
uv sync
```

### PDF Support (Optional)

To enable PDF to Markdown conversion, install with the `pdf` extra (requires PyTorch):

```bash
pip install "contextpack[pdf]"
# or with uv
uv pip install "contextpack[pdf]"
```

## CLI Usage

### Get context to stdout
Extract Markdown directly to your terminal.

```bash
uv run contextpack https://docs.ros.org/en/humble/Concepts.html
```

### Save context to folder
Write the extracted content to a `.contextpack/` folder.

```bash
uv run contextpack https://docs.ros.org/en/humble/Concepts.html --write
```

### Convert PDF to Markdown
Download a PDF and convert it using `marker-pdf`. Results are saved to `.contextpack/`.

```bash
uv run contextpack pdf https://arxiv.org/pdf/2303.08774.pdf
```

### Clear stored context
Delete the `.contextpack/` folder and all its contents.

```bash
uv run contextpack --clear
```

## Python Library Usage

```python
from contextpack import get_url_context

content = get_url_context("https://docs.ros.org/en/humble/Concepts.html")
print(content)
```

## Architecture

- `api.py`: Core logic for fetching, scraping, and PDF conversion.
- `scraper.py`: Content extraction wrapper around `trafilatura`.
- `cli.py`: Simplified CLI interface.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the terms provided in the [LICENSE](LICENSE) file.
