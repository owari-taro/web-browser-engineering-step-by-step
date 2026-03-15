import pytest
import sys
from pathlib import Path


from mybrowser.main import URL


def test_extracts_scheme_hostname_and_default_path():
    url = URL("https://example.com")

    assert url.scheme == "https"
    assert url.hostname == "example.com"
    assert url.path == "/"


def test_extracts_path_when_present():
    url = URL("http://example.com/docs/index.html?lang=en#top")

    assert url.scheme == "http"
    assert url.hostname == "example.com"
    assert url.path == "/docs/index.html"


@pytest.mark.parametrize(
    "raw_url, message",
    [
        ("example.com/path", "URL must include a scheme"),
        ("ftp://example.com/file.txt", "Only http and https URLs are supported"),
        ("https:///missing-host", "URL must include a hostname"),
    ],
)
def test_invalid_urls_raise_value_error(raw_url, message):
    with pytest.raises(ValueError, match=message):
        URL(raw_url)
