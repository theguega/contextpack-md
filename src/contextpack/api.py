import os
import httpx
from typing import Optional
from .scraper import fetch_and_scrape

def get_url_context(url: str) -> Optional[str]:
    """
    Fetches and scrapes a single URL to return clean Markdown.
    """
    return fetch_and_scrape(url)

def download_pdf(url: str, save_path: str) -> bool:
    """
    Downloads a PDF file from a URL.
    """
    try:
        with httpx.Client(follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return False

def convert_pdf_to_markdown(pdf_path: str) -> Optional[str]:
    """
    Converts a PDF file to Markdown using marker-pdf.
    """
    try:
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        from marker.output import text_from_rendered

        converter = PdfConverter(
            artifact_dict=create_model_dict(),
        )
        rendered = converter(pdf_path)
        text, _, _ = text_from_rendered(rendered)
        return text
    except ImportError:
        print("Error: marker-pdf is not installed. Please install it with 'pip install \"contextpack[pdf]\"'")
        return None
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return None
