from bs4 import BeautifulSoup
from urllib.parse import urljoin


def canonical_url(response):
    link = response.css('link[rel="canonical"]::attr(href)').get()
    if link:
        return urljoin(response.url, link)
    return response.url


def get_breadcrumbs(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    selectors = [
        "nav[aria-label='Breadcrumb'] a",
        "ol.breadcrumb li a",
        "nav.breadcrumb li a",
    ]
    crumbs: list[str] = []
    for sel in selectors:
        for a in soup.select(sel):
            text = a.get_text(strip=True)
            if text:
                crumbs.append(text)
        if crumbs:
            break
    return crumbs


def get_headings(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    results = []
    for level in [1, 2, 3]:
        for tag in soup.find_all(f"h{level}"):
            text = tag.get_text(strip=True)
            if text:
                results.append({"level": level, "text": text})
    return results