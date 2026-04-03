from typing import Optional

import trafilatura


def extract_content(html: str, url: str) -> Optional[str]:
    """
    Extracts readable markdown from HTML.
    """
    return trafilatura.extract(
        html,
        url=url,
        output_format="markdown",
        include_links=True,
        include_images=False,
    )


def fetch_and_scrape(url: str, timeout: int = 10) -> Optional[str]:
    """
    Downloads and extracts content from a URL.
    """
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return None
    return extract_content(downloaded, url)
