import typer
import os
from .api import query_url, ask_web, summarize_context
from .scraper import extract_pdf_content, fetch_and_scrape

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
def summarize(
    source: str,
    task: str = typer.Option(..., help="The specific user task to summarize the context for"),
    model: str = typer.Option("gpt-3.5-turbo", help="The LiteLLM supported model string (e.g. gpt-4o, ollama/llama3, etc.)")
):
    """
    Condense extracted documents or PDFs into highly relevant context for a specific user task.
    """
    typer.echo(f"📝 Summarizing source: '{source}' for task: '{task}' using model: '{model}'...")

    text = None

    # Check if source is a URL or a local file path
    if source.startswith("http://") or source.startswith("https://"):
        text = fetch_and_scrape(source)
    else:
        # Check if local file exists
        if not os.path.exists(source):
            typer.echo(f"❌ Error: Local file not found: {source}")
            raise typer.Exit(code=1)

        if source.lower().endswith(".pdf"):
            text = extract_pdf_content(source)
        else:
            try:
                with open(source, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                typer.echo(f"❌ Error reading file {source}: {e}")
                raise typer.Exit(code=1)

    if not text:
        typer.echo("❌ Error: Could not extract content from the source.")
        raise typer.Exit(code=1)

    result = summarize_context(text, task, model)

    typer.echo("\n--- Final Summarized Context ---\n")
    typer.echo(result.context)

if __name__ == "__main__":
    app()
