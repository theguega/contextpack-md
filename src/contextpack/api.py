from typing import List
from urllib.parse import urlparse
from .models import ContextPackResult, ContextSource, ContextChunk
from .crawler import crawl_documentation
from .search import search_duckduckgo
from .scraper import fetch_and_scrape
from .chunker import split_into_chunks
from .ranker import rank_chunks
from .formatter import format_context_pack
from .pdf import extract_pdf_text
from .arxiv import fetch_arxiv_data
from .repo import ingest_repo_files
import os

def ingest_repo(repo_url: str) -> ContextPackResult:
    """
    Ingests a repository from a URL, extracting text-based code files.
    """
    files_content = ingest_repo_files(repo_url)

    sources = []
    all_chunks = []

    parsed_url = urlparse(repo_url)
    domain = parsed_url.netloc

    sources.append(ContextSource(url=repo_url, domain=domain))

    for file_path, content in files_content.items():
        # Prepend file path to content for context
        file_text = f"File: {file_path}\n\n{content}"
        chunks = split_into_chunks(file_text)
        for chunk_text in chunks:
            all_chunks.append(ContextChunk(text=chunk_text, source_url=repo_url))

    result = ContextPackResult(
        query=f"Repository ingestion for {repo_url}",
        sources=sources,
        chunks=all_chunks,
        context=""
    )
    result.context = format_context_pack(result)
    return result

def query_url(url: str, max_depth: int = 2, max_pages: int = 10) -> ContextPackResult:
    """
    Extracts documentation context starting from a given page.
    """
    content_map = crawl_documentation(url, max_depth=max_depth, max_pages=max_pages)
    
    sources = []
    all_chunks = []
    
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    for page_url, content in content_map.items():
        sources.append(ContextSource(url=page_url, domain=domain))
        chunks = split_into_chunks(content)
        for chunk_text in chunks:
            all_chunks.append(ContextChunk(text=chunk_text, source_url=page_url))
            
    # For query_url, we just take the first chunks or a sample if too many, 
    # but the prompt says aggregate content. 
    # If it's for documentation, maybe we just return top chunks by some relevance to the URL itself 
    # or just return them all if small enough.
    # Let's use the first part of the first page as a "query" for ranking if we have too many.
    query = url
    top_chunks = rank_chunks(query, all_chunks, top_k=20) if len(all_chunks) > 20 else all_chunks
    
    result = ContextPackResult(
        query=f"Documentation for {url}",
        sources=sources,
        chunks=top_chunks,
        context=""
    )
    result.context = format_context_pack(result)
    return result

def read_pdf(path_or_url: str) -> ContextPackResult:
    """
    Extracts text from a local PDF or a remote PDF URL.
    """
    text = extract_pdf_text(path_or_url)

    parsed = urlparse(path_or_url)
    domain = parsed.netloc if parsed.scheme in ("http", "https") else "local"
    url = path_or_url if parsed.scheme in ("http", "https") else f"file://{os.path.abspath(path_or_url)}"

    source = ContextSource(url=url, domain=domain, title=os.path.basename(path_or_url))
    chunks = split_into_chunks(text)

    context_chunks = [ContextChunk(text=c, source_url=url) for c in chunks]

    result = ContextPackResult(
        query=f"PDF extraction for {path_or_url}",
        sources=[source],
        chunks=context_chunks,
        context=""
    )
    result.context = format_context_pack(result)
    return result

def query_arxiv(id_or_query: str) -> ContextPackResult:
    """
    Fetches an arXiv paper by ID or search query and extracts its content.
    """
    data = fetch_arxiv_data(id_or_query)
    if not data:
        # Fallback empty result
        result = ContextPackResult(query=id_or_query, sources=[], chunks=[], context="No arXiv results found.")
        result.context = format_context_pack(result)
        return result

    pdf_url = data.get("pdf_url")
    if not pdf_url:
        result = ContextPackResult(query=id_or_query, sources=[], chunks=[], context="arXiv entry found but no PDF linked.")
        result.context = format_context_pack(result)
        return result

    text = extract_pdf_text(pdf_url)

    source = ContextSource(url=data["entry_id"], domain="arxiv.org", title=data["title"])
    chunks = split_into_chunks(text)

    context_chunks = [ContextChunk(text=c, source_url=data["entry_id"]) for c in chunks]

    # We might want to inject the title and summary into the first chunk or metadata, but for now just add them
    summary_chunk = ContextChunk(text=f"Title: {data['title']}\n\nAbstract: {data['summary']}", source_url=data["entry_id"])
    context_chunks.insert(0, summary_chunk)

    result = ContextPackResult(
        query=f"arXiv query for {id_or_query}",
        sources=[source],
        chunks=context_chunks,
        context=""
    )
    result.context = format_context_pack(result)
    return result

def ask_web(question: str) -> ContextPackResult:
    """
    Automatically gathers relevant context from the web.
    """
    urls = search_duckduckgo(question)
    
    sources = []
    all_chunks = []
    
    for url in urls:
        content = fetch_and_scrape(url)
        if content:
            domain = urlparse(url).netloc
            sources.append(ContextSource(url=url, domain=domain))
            chunks = split_into_chunks(content)
            for chunk_text in chunks:
                all_chunks.append(ContextChunk(text=chunk_text, source_url=url))
                
    top_chunks = rank_chunks(question, all_chunks, top_k=10)
    
    result = ContextPackResult(
        query=question,
        sources=sources,
        chunks=top_chunks,
        context=""
    )
    result.context = format_context_pack(result)
    return result
