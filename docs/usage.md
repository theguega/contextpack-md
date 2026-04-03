# 📖 Usage

`contextpack` can be used both as a CLI tool and a Python library.

## CLI Usage

### Basic Extraction
Extract content from a URL directly to your terminal.
```bash
uvx contextpack web https://docs.python.org/3/
```

### Save to Cache
Store the output in `~/.contextpack/` with a timestamped name.
```bash
uvx contextpack web https://docs.python.org/3/ --write
```

### PDF to Markdown
Download and convert a PDF. This requires `marker-pdf` (automatically installed if using the `pdf` extra).
```bash
uvx contextpack pdf https://arxiv.org/pdf/1706.03762.pdf
```

### Clearing the Cache
Remove all stored content in `~/.contextpack/`.
```bash
uvx contextpack clear
```

---

## Python API Usage

If you're building your own tool, you can use `contextpack` programmatically.

```python
from contextpack import get_url_context

# Fetch and scrape a URL
content = get_url_context("https://python.org")

if content:
    print(content)
```
