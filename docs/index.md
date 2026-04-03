# 📦 contextpack

A dead-simple tool to extract high-quality Markdown from any URL for LLMs.

## 🚀 Quick Start

```bash
# Get context to stdout
uvx contextpack https://docs.python.org/3/

# Download a PDF and convert to Markdown
uvx contextpack pdf https://arxiv.org/pdf/1706.03762.pdf
```

## ✨ Features

- **Single Purpose**: Get clean, LLM-ready Markdown from a URL.
- **PDF Support**: Convert online PDFs to high-quality Markdown using `marker-pdf`.
- **Optional Local Storage**: Save results to a `.contextpack` folder.
- **Zero Configuration**: No complex ranking, crawling, or embedding setups.
