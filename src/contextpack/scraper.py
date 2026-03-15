import trafilatura
from typing import Optional
from pypdf import PdfReader
import io
import requests

def extract_pdf_content(filepath_or_url: str) -> Optional[str]:
    """
    Extracts text from a local PDF file or a PDF URL.
    """
    try:
        if filepath_or_url.startswith("http://") or filepath_or_url.startswith("https://"):
            response = requests.get(filepath_or_url, stream=True)
            response.raise_for_status()
            reader = PdfReader(io.BytesIO(response.content))
        else:
            reader = PdfReader(filepath_or_url)

        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None

def extract_content(html: str, url: str) -> Optional[str]:
    """
    Extracts readable markdown from HTML.
    """
    return trafilatura.extract(
        html,
        url=url,
        output_format="markdown",
        include_links=True,
        include_images=False
    )

def fetch_and_scrape(url: str, timeout: int = 10) -> Optional[str]:
    """
    Downloads and extracts content from a URL.
    """
    if url.lower().endswith(".pdf"):
        return extract_pdf_content(url)

    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return None
    return extract_content(downloaded, url)
