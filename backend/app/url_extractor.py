import httpx
from bs4 import BeautifulSoup
from readability import Document

from .config import settings


async def fetch_and_extract_article(url: str) -> str:
    timeout = httpx.Timeout(settings.request_timeout_seconds)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()

    doc = Document(response.text)
    article_html = doc.summary(html_partial=True)
    soup = BeautifulSoup(article_html, 'html.parser')
    text = ' '.join(soup.get_text(separator=' ').split())
    return text[: settings.max_text_length]
