from __future__ import annotations

from urllib.parse import urlparse


def normalize_url(raw_url: str) -> str | None:
    """Нормализует URL, оставляя только схему и домен."""
    try:
        parsed = urlparse(raw_url)

        if not parsed.scheme or not parsed.netloc:
            return None

        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return None
