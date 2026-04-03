from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import typer

from .api import convert_pdf_to_markdown, download_pdf, get_url_context

app = typer.Typer(add_completion=False)

CONTEXTPACK_DIR = Path.home() / ".contextpack-md"


def clean_domain(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path.split("/")[-1]
    return domain.replace(".", "_").replace("/", "_")


@app.command()
def web(
    url: str = typer.Argument(help="URL to extract context from"),
    write: bool = typer.Option(
        False, "--write", "-w", help="Write result to .contextpack-md folder"
    ),
    output_dir: Optional[Path] = typer.Argument(None, help="Output directory path"),
):
    """
    Extract context from a web URL and optionally write it to a file.
    """
    if not url:
        typer.echo("Error: Please provide a URL or use --clear")
        raise typer.Exit(code=1)

    typer.echo(f"🔍 Fetching context from: {url}...")
    content = get_url_context(url)

    if not content:
        typer.echo("❌ Error: Could not extract content from URL.")
        raise typer.Exit(code=1)

    if write:
        dir = output_dir if output_dir else CONTEXTPACK_DIR
        dir.mkdir(parents=True, exist_ok=True)
        domain = clean_domain(url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{domain}_{timestamp}.md"
        filepath = dir / filename

        with filepath.open("w", encoding="utf-8") as f:
            f.write(content)

        typer.echo(f"💾 Content written to: {filepath}")
    else:
        typer.echo("\n--- Content Start ---\n")
        typer.echo(content)
        typer.echo("\n--- Content End ---\n")


@app.command()
def clear():
    """
    Clear the contextpack-md cache directory.
    """
    if CONTEXTPACK_DIR.exists():
        files = list(CONTEXTPACK_DIR.glob("*"))
        typer.echo(f"🗑️  Clearing {len(files)} item from {CONTEXTPACK_DIR}")
        for file in files:
            if file.is_file():
                file.unlink()
    else:
        typer.echo(f"❌ Cache directory {CONTEXTPACK_DIR} does not exist.")


@app.command()
def pdf(
    url: str = typer.Argument(..., help="URL to the PDF file"),
    output_dir: Optional[Path] = typer.Argument(None, help="Output directory path"),
):
    """
    Download a PDF and convert it to Markdown using marker-pdf.
    """
    dir = output_dir or CONTEXTPACK_DIR
    dir.mkdir(parents=True, exist_ok=True)

    domain = clean_domain(url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"{domain}_{timestamp}.pdf"
    pdf_path = dir / pdf_filename

    typer.echo(f"📥 Downloading PDF from: {url}...")
    if not download_pdf(url, pdf_path):
        typer.echo("❌ Error: Failed to download PDF.")
        raise typer.Exit(code=1)

    typer.echo(
        "⚙️  Converting PDF to Markdown... (This process uses ML and can take ~0.2s/page)"
    )
    markdown_content = convert_pdf_to_markdown(pdf_path)

    if not markdown_content:
        typer.echo("❌ Error: Failed to convert PDF to Markdown.")
        raise typer.Exit(code=1)

    md_filename = f"{domain}_{timestamp}.md"
    md_path = dir / md_filename

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    typer.echo(f"✅ Successfully converted PDF. Result saved to: {md_path}")


if __name__ == "__main__":
    app()
