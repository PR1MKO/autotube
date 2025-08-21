import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse, urlunparse, parse_qsl, urlencode

import scrapy

from excelcrawler.utils import extract as extract_utils
from excelcrawler.utils import html as html_utils
from excelcrawler.utils.hashing import hash_content

ALLOW_RE = re.compile(r"^https://support\.microsoft\.com/([a-z]{2}-[a-z]{2})/excel/.*$")
DENY_EXT = re.compile(r"\.(png|jpg|gif|svg|css|js|mp4|webm|zip|pptx|xlsx|pdf)$", re.I)


def strip_tracking(url: str) -> str:
    parsed = urlparse(url)
    if DENY_EXT.search(parsed.path):
        return ""
    query = [
        (k, v)
        for k, v in parse_qsl(parsed.query)
        if not (k.lower().startswith("wt.") or k.lower() == "ocid")
    ]
    parsed = parsed._replace(query=urlencode(query), fragment="")
    return urlunparse(parsed)


class SupportExcelSpider(scrapy.Spider):
    name = "support_excel"
    allowed_domains = ["support.microsoft.com"]
    start_urls = [
        "https://support.microsoft.com/en-us/excel",
        "https://support.microsoft.com/hu-hu/excel",
    ]

    def parse(self, response):
        if ALLOW_RE.match(response.url):
            yield from self.parse_article(response)
        for href in response.css("a::attr(href)").getall():
            url = strip_tracking(urljoin(response.url, href))
            if url and ALLOW_RE.match(url):
                yield scrapy.Request(url, callback=self.parse)

    def parse_article(self, response):
        html = response.text
        canonical = html_utils.canonical_url(response)
        m = ALLOW_RE.match(response.url)
        locale = m.group(1) if m else "other"
        title = response.css("title::text").get() or ""
        description = response.css('meta[name="description"]::attr(content)').get() or ""
        breadcrumbs = html_utils.get_breadcrumbs(html)
        headings = html_utils.get_headings(html)
        text, tables, code_blocks = extract_utils.extract_content(html, response.url)
        links_out = []
        for href in response.css("a::attr(href)").getall():
            abs_url = urljoin(response.url, strip_tracking(href))
            if abs_url.startswith("http"):
                links_out.append(abs_url)
        links_out = sorted(set(links_out))
        last_modified = response.headers.get("Last-Modified", b"").decode()
        etag = response.headers.get("ETag", b"").decode()
        sha = hash_content(text, html)
        slug = sha[:16]
        Path("data/pages_raw").mkdir(parents=True, exist_ok=True)
        html_path = f"data/pages_raw/{slug}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        yield {
            "url": response.url,
            "canonical_url": canonical,
            "locale": locale.lower(),
            "source": "support",
            "title": title.strip(),
            "description": description.strip(),
            "breadcrumbs": breadcrumbs,
            "headings": headings,
            "text_md": text,
            "code_blocks": code_blocks,
            "tables": tables,
            "links_out": links_out,
            "last_modified": last_modified,
            "etag": etag,
            "html_path": html_path,
            "sha256": sha,
            "fetched_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        }