# 📦 contextpack-md

<p align="center">
  <a href="https://github.com/theguega/contextpack-md/actions/workflows/release.yml"><img src="https://github.com/theguega/contextpack-md/actions/workflows/release.yml/badge.svg" alt="Release Status"></a>
  <a href="https://theguega.github.io/contextpack-md/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg" alt="Documentation"></a>
  <a href="https://pypi.org/project/contextpack-md/"><img src="https://img.shields.io/pypi/v/contextpack-md.svg" alt="PyPI version"></a>
  <a href="https://github.com/theguega/contextpack-md/blob/main/LICENSE"><img src="https://img.shields.io/github/license/theguega/contextpack-md.svg" alt="License"></a>
</p>

A dead-simple tool to extract high-quality Markdown from any URL or PDF, optimized for LLMs.

## 🚀 Quick Start

Extract clean, LLM-ready Markdown from any URL in seconds.

```bash
# Using uv (recommended)
uvx contextpack-md web https://docs.python.org/3/

# Download and convert PDF
uvx contextpack-md pdf https://arxiv.org/pdf/1706.03762.pdf
```

## ✨ Key Features

- **🎯 LLM-Ready Output**: Clean, readable Markdown with links, but no junk.
- **📄 PDF Support**: High-fidelity PDF-to-Markdown conversion (via `marker-pdf`).
- **📂 Local Caching**: Optional timestamped local storage in `~/.contextpack-md/`.
- **⚡ Fast & Lean**: Built on top of `trafilatura` for superior extraction speed and quality.

## 🛠️ Installation

```bash
pip install contextpack-md

# For PDF support (requires PyTorch)
pip install "contextpack-md[pdf]"
```

## 📖 Documentation

Full documentation is available at [https://theguega.github.io/contextpack-md/](https://theguega.github.io/contextpack-md/).

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## ⚖️ License

MIT License. See [LICENSE](LICENSE) for more information.
