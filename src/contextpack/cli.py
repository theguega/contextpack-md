import typer
from .api import query_url, ask_web, ingest_repo

app = typer.Typer(add_completion=False)

@app.command()
def query(
    url: str,
    depth: int = typer.Option(2, help="Crawl depth (0 for only this page, 1 for immediate links, etc.)"),
    max_pages: int = typer.Option(10, help="Maximum number of pages to crawl")
):
    """
    Extract documentation context starting from a given page.
    """
    typer.echo(f"🔍 Querying documentation at: {url} (depth={depth}, max_pages={max_pages})")
    result = query_url(url, max_depth=depth, max_pages=max_pages)
    typer.echo(result.context)

@app.command()
def ask(question: str):
    """
    Automatically gather relevant context from the web.
    """
    typer.echo(f"🔎 Searching the web for: '{question}'...")
    result = ask_web(question)
    typer.echo("\n--- Final Context Pack ---\n")
    typer.echo(result.context)

@app.command()
def repo(url: str):
    """
    Ingest a code repository and extract text-based files.
    """
    typer.echo(f"📦 Ingesting repository: {url}...")
    try:
        result = ingest_repo(url)
        typer.echo("\n--- Final Context Pack ---\n")
        typer.echo(result.context)
    except Exception as e:
        typer.echo(f"❌ Error: {e}")

if __name__ == "__main__":
    app()
