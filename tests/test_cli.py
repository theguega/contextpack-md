from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from contextpack.cli import app, clean_domain

runner = CliRunner()

def test_clean_domain():
    assert clean_domain("https://example.com/path") == "example_com"
    assert clean_domain("https://test.example.org") == "test_example_org"

def test_web_no_url():
    result = runner.invoke(app, ["web"])
    assert result.exit_code == 1
    assert "Error: Please provide a URL or use --clear" in result.stdout

def test_web_success():
    url = "https://example.com"
    content = "# Mock Content"
    
    with patch("contextpack.cli.get_url_context") as mock_get:
        mock_get.return_value = content
        result = runner.invoke(app, ["web", url])
        
        assert result.exit_code == 0
        assert "🔍 Fetching context from: https://example.com..." in result.stdout
        assert "--- Content Start ---" in result.stdout
        assert content in result.stdout
        mock_get.assert_called_once_with(url)

def test_web_write(tmp_path):
    url = "https://example.com"
    content = "# Mock Content"
    
    # Mocking CONTEXTPACK_DIR in cli.py
    with patch("contextpack.cli.CONTEXTPACK_DIR", tmp_path):
        with patch("contextpack.cli.get_url_context") as mock_get:
            mock_get.return_value = content
            result = runner.invoke(app, ["web", url, "--write"])
            
            assert result.exit_code == 0
            assert f"💾 Content written to:" in result.stdout
            
            # Find the written file
            written_files = list(tmp_path.glob("example_com_*.md"))
            assert len(written_files) == 1
            assert written_files[0].read_text() == content

def test_web_clear(tmp_path):
    # Setup a dummy .contextpack folder
    (tmp_path / "dummy.md").write_text("dummy")
    
    with patch("contextpack.cli.CONTEXTPACK_DIR", tmp_path):
        result = runner.invoke(app, ["web", "--clear"])
        
        assert result.exit_code == 0
        assert "🗑️ Deleted" in result.stdout
        assert not tmp_path.exists()

def test_pdf_success(tmp_path):
    url = "https://example.com/test.pdf"
    content = "# PDF Markdown"
    
    with patch("contextpack.cli.CONTEXTPACK_DIR", tmp_path):
        with patch("contextpack.cli.download_pdf") as mock_download:
            with patch("contextpack.cli.convert_pdf_to_markdown") as mock_convert:
                mock_download.return_value = True
                mock_convert.return_value = content
                
                result = runner.invoke(app, ["pdf", url])
                
                assert result.exit_code == 0
                assert "📥 Downloading PDF" in result.stdout
                assert "✅ Successfully converted PDF" in result.stdout
                
                # Check if markdown file was created
                written_files = list(tmp_path.glob("example_com_*.md"))
                assert len(written_files) == 1
                assert written_files[0].read_text() == content
