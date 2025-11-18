from __future__ import annotations

from urllib.parse import urlparse

from bs4 import BeautifulSoup
from validators import url as validate_url


def normalize_url(raw_url: str) -> str | None:
    """Нормализует URL, оставляя только схему и домен."""
    try:
        parsed = urlparse(raw_url)

        if not parsed.scheme or not parsed.netloc:
            return None

        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return None


def is_valid_url(raw_url: str) -> bool:
    """Проверяет URL с помощью библиотеки validators."""
    return bool(validate_url(raw_url))


def parse_seo_data(html: str) -> dict[str, str | None]:
    """Извлекает SEO-данные (h1, title, description) из HTML."""
    soup = BeautifulSoup(html, "html.parser")

    def extract_text(tag):
        return tag.get_text(strip=True) if tag else None

    h1 = soup.find("h1")
    title = soup.find("title")
    description = soup.find("meta", attrs={"name": "description"})

    return {
        "h1": extract_text(h1),
        "title": extract_text(title),
        "description": (
            description.get("content", "").strip() if description else None
        ),
    }
