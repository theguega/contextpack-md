from pathlib import Path
from unittest.mock import MagicMock, patch
from contextpack.api import download_pdf, get_url_context

def test_get_url_context():
    url = "https://example.com"
    content = "# Content"
    
    with patch("contextpack.api.fetch_and_scrape") as mock_fetch:
        mock_fetch.return_value = content
        result = get_url_context(url)
        assert result == content
        mock_fetch.assert_called_once_with(url)

def test_download_pdf_success(tmp_path):
    url = "https://example.com/test.pdf"
    save_path = tmp_path / "test.pdf"
    content = b"PDF content"
    
    with patch("httpx.Client") as mock_client:
        mock_instance = mock_client.return_value.__enter__.return_value
        mock_response = MagicMock()
        mock_response.content = content
        mock_response.raise_for_status = MagicMock()
        mock_instance.get.return_value = mock_response
        
        result = download_pdf(url, save_path)
        
        assert result is True
        assert save_path.read_bytes() == content
        mock_instance.get.assert_called_once_with(url)

def test_download_pdf_failure(tmp_path):
    url = "https://example.com/test.pdf"
    save_path = tmp_path / "test.pdf"
    
    with patch("httpx.Client") as mock_client:
        mock_instance = mock_client.return_value.__enter__.return_value
        mock_instance.get.side_effect = Exception("Network error")
        
        result = download_pdf(url, save_path)
        
        assert result is False
        assert not save_path.exists()
