from urllib.parse import urlsplit


class URL:
    def __init__(self, url):
        self.url = url
        parts = urlsplit(url)
        if not parts.scheme:
            raise ValueError("URL must include a scheme")
        if parts.scheme not in ["http", "https"]:
            raise ValueError("Only http and https URLs are supported")
        if not parts.hostname:
            raise ValueError("URL must include a hostname")

        self.scheme = parts.scheme
        self.hostname = parts.hostname
        self.path = parts.path or "/"

    