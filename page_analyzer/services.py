from __future__ import annotations

from urllib.parse import urlparse


def normalize_url(raw_url: str) -> str | None:
    """Normalizes URL keeping only scheme and domain."""
    try:
        parsed = urlparse(raw_url)

        if not parsed.scheme or not parsed.netloc:
            return None

        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return None

