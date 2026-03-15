from typing import List
from urllib.parse import urlparse
from .models import ContextPackResult, ContextSource, ContextChunk
from .crawler import crawl_documentation
from .search import search_duckduckgo
from .scraper import fetch_and_scrape
from .chunker import split_into_chunks
from .ranker import rank_chunks
from .formatter import format_context_pack
from .summarizer import summarize_text

def summarize_context(context: str, task: str, model: str) -> ContextPackResult:
    """
    Condenses the provided context based on a task using an LLM.
    """
    summary = summarize_text(context, task, model)

    result = ContextPackResult(
        query=task,
        sources=[],
        chunks=[ContextChunk(text=summary, source_url="summary")],
        context=summary
    )
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
