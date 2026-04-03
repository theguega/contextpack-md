# Contributing to contextpack

First off, thank you for considering contributing to `contextpack`! It's people like you who make it a great tool for everyone.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs
* Check the [GitHub Issues](https://github.com/theguega/contextpack/issues) to see if the bug has already been reported.
* If not, open a new issue. Include a clear title, a detailed description, and a way to reproduce the error.

### Suggesting Enhancements
* Open a new issue with the "enhancement" label.
* Describe the feature and why it would be useful.

### Pull Requests
1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code follows the existing style (see [Development Setup](#development-setup)).
5. Issue that Pull Request!

## Development Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone https://github.com/theguega/contextpack.git
cd contextpack

# Sync dependencies
uv sync --all-groups

# Run the CLI in development
uv run contextpack --help
```

### Linting & Formatting

We use `ruff` for linting and formatting. Please run it before submitting a PR:

```bash
uv run ruff check .
uv run ruff format .
```

### Testing

(Tests are being integrated. If you add a feature, please include a `tests/` directory with `pytest` cases.)

## Style Guide

* Use Type Hints for all function signatures.
* Follow PEP 8 conventions.
* Keep functions small and focused on a single task.
* Write descriptive docstrings for all public APIs.
