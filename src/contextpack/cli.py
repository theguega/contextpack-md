import typer
import os
import shutil
from datetime import datetime
from urllib.parse import urlparse
from typing import Optional
from .api import get_url_context, download_pdf, convert_pdf_to_markdown

app = typer.Typer(add_completion=False)

CONTEXTPACK_DIR = ".contextpack"

def clean_domain(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path.split('/')[-1]
    return domain.replace('.', '_').replace('/', '_')

@app.command()
def main(
    url: Optional[str] = typer.Argument(None, help="URL to extract context from"),
    write: bool = typer.Option(False, "--write", "-w", help="Write result to .contextpack folder"),
    clear: bool = typer.Option(False, "--clear", help="Delete the .contextpack folder")
):
    """
    contextpack: Extract clean Markdown from any URL for LLMs.
    """
    if clear:
        if os.path.exists(CONTEXTPACK_DIR):
            shutil.rmtree(CONTEXTPACK_DIR)
            typer.echo(f"🗑️ Deleted {CONTEXTPACK_DIR}/")
        else:
            typer.echo("ℹ️ No .contextpack/ folder found.")
        return

    if not url:
        typer.echo("Error: Please provide a URL or use --clear")
        raise typer.Exit(code=1)

    typer.echo(f"🔍 Fetching context from: {url}...")
    content = get_url_context(url)

    if not content:
        typer.echo("❌ Error: Could not extract content from URL.")
        raise typer.Exit(code=1)

    if write:
        if not os.path.exists(CONTEXTPACK_DIR):
            os.makedirs(CONTEXTPACK_DIR)
        
        domain = clean_domain(url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{domain}_{timestamp}.md"
        filepath = os.path.join(CONTEXTPACK_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        typer.echo(f"💾 Content written to: {filepath}")
    else:
        typer.echo("\n--- Content Start ---\n")
        typer.echo(content)
        typer.echo("\n--- Content End ---\n")

@app.command()
def pdf(
    url: str = typer.Argument(..., help="URL to the PDF file")
):
    """
    Download a PDF and convert it to Markdown using marker-pdf.
    """
    if not os.path.exists(CONTEXTPACK_DIR):
        os.makedirs(CONTEXTPACK_DIR)

    domain = clean_domain(url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"{domain}_{timestamp}.pdf"
    pdf_path = os.path.join(CONTEXTPACK_DIR, pdf_filename)
    
    typer.echo(f"📥 Downloading PDF from: {url}...")
    if not download_pdf(url, pdf_path):
        typer.echo("❌ Error: Failed to download PDF.")
        raise typer.Exit(code=1)

    typer.echo(f"⚙️  Converting PDF to Markdown... (This process uses ML and can take ~0.2s/page)")
    markdown_content = convert_pdf_to_markdown(pdf_path)

    if not markdown_content:
        typer.echo("❌ Error: Failed to convert PDF to Markdown.")
        raise typer.Exit(code=1)

    md_filename = f"{domain}_{timestamp}.md"
    md_path = os.path.join(CONTEXTPACK_DIR, md_filename)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    typer.echo(f"✅ Successfully converted PDF. Result saved to: {md_path}")

if __name__ == "__main__":
    app()
