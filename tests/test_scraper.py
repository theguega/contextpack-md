from unittest.mock import patch

from contextpack_md.scraper import extract_content, fetch_and_scrape


def test_extract_content():
    html = "<html><body><h1>Hello</h1><p>World</p></body></html>"
    url = "https://example.com"

    with patch("trafilatura.extract") as mock_extract:
        mock_extract.return_value = "# Hello\n\nWorld"
        result = extract_content(html, url)
        assert result == "# Hello\n\nWorld"
        mock_extract.assert_called_once_with(
            html,
            url=url,
            output_format="markdown",
            include_links=True,
            include_images=False,
        )


def test_fetch_and_scrape_success():
    url = "https://example.com"
    html = "<html><body>Test</body></html>"
    markdown = "Test"

    with patch("trafilatura.fetch_url") as mock_fetch:
        with patch("contextpack_md.scraper.extract_content") as mock_extract:
            mock_fetch.return_value = html
            mock_extract.return_value = markdown

            result = fetch_and_scrape(url)

            assert result == markdown
            mock_fetch.assert_called_once_with(url)
            mock_extract.assert_called_once_with(html, url)


def test_fetch_and_scrape_failure():
    url = "https://example.com"

    with patch("trafilatura.fetch_url") as mock_fetch:
        mock_fetch.return_value = None

        result = fetch_and_scrape(url)

        assert result is None
        mock_fetch.assert_called_once_with(url)
