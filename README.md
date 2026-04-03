# 📦 contextpack

<p align="center">
  <a href="https://github.com/theguega/contextpack/actions/workflows/release.yml"><img src="https://github.com/theguega/contextpack/actions/workflows/release.yml/badge.svg" alt="Release Status"></a>
  <a href="https://theguega.github.io/contextpack/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg" alt="Documentation"></a>
  <a href="https://pypi.org/project/contextpack/"><img src="https://img.shields.io/pypi/v/contextpack.svg" alt="PyPI version"></a>
  <a href="https://github.com/theguega/contextpack/blob/main/LICENSE"><img src="https://img.shields.io/github/license/theguega/contextpack.svg" alt="License"></a>
</p>

A dead-simple tool to extract high-quality Markdown from any URL or PDF, optimized for LLMs.

## 🚀 Quick Start

Extract clean, LLM-ready Markdown from any URL in seconds.

```bash
# Using uv (recommended)
uvx contextpack web https://docs.python.org/3/

# Download and convert PDF
uvx contextpack pdf https://arxiv.org/pdf/1706.03762.pdf
```

## ✨ Key Features

- **🎯 LLM-Ready Output**: Clean, readable Markdown with links, but no junk.
- **📄 PDF Support**: High-fidelity PDF-to-Markdown conversion (via `marker-pdf`).
- **📂 Local Caching**: Optional timestamped local storage in `~/.contextpack/`.
- **⚡ Fast & Lean**: Built on top of `trafilatura` for superior extraction speed and quality.

## 🛠️ Installation

```bash
pip install contextpack

# For PDF support (requires PyTorch)
pip install "contextpack[pdf]"
```

## 📖 Documentation

Full documentation is available at [https://theguega.github.io/contextpack/](https://theguega.github.io/contextpack/).

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## ⚖️ License

MIT License. See [LICENSE](LICENSE) for more information.
