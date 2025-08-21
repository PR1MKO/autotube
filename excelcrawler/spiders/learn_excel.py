import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse, urlunparse, parse_qsl, urlencode
from typing import Optional

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from excelcrawler.utils import extract as extract_utils
from excelcrawler.utils import html as html_utils
from excelcrawler.utils.hashing import hash_content

ALLOW = re.compile(
    r"^https://learn\.microsoft\.com/([a-z]{2}-[a-z]{2})/"
    r"(troubleshoot/microsoft-365-apps/excel/.*"
    r"|office/vba/.*excel.*)$",
    re.I
)
DENY_EXT = re.compile(r"\.(png|jpg|gif|svg|css|js|mp4|webm|zip|pptx|xlsx|pdf)$", re.I)


def strip_tracking(url: str) -> Optional[str]:
    parsed = urlparse(url)
    if DENY_EXT.search(parsed.path):
        return None
    query = [
        (k, v)
        for k, v in parse_qsl(parsed.query)
        if not (k.lower().startswith("wt.") or k.lower() == "ocid")
    ]
    parsed = parsed._replace(query=urlencode(query), fragment="")
    return urlunparse(parsed)


class LearnExcelSpider(CrawlSpider):
    name = "learn_excel"
    allowed_domains = ["learn.microsoft.com"]
    start_urls = [
        "https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/",
        "https://learn.microsoft.com/hu-hu/troubleshoot/microsoft-365-apps/excel/",
        # Optional dev docs:
        # "https://learn.microsoft.com/en-us/office/vba/api/overview/excel",
        # "https://learn.microsoft.com/hu-hu/office/vba/api/overview/excel",
    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=ALLOW.pattern,
                process_value=strip_tracking,
            ),
            callback="parse_article",
            follow=True,
        )
    ]

    def parse_start_url(self, response):
        yield from self.parse_article(response)

    def parse_article(self, response):
        html = response.text
        canonical = html_utils.canonical_url(response)
        m = ALLOW.match(response.url)
        locale = m.group(1) if m else "other"
        title = response.css("title::text").get() or ""
        description = response.css('meta[name="description"]::attr(content)').get() or ""
        breadcrumbs = html_utils.get_breadcrumbs(html)
        headings = html_utils.get_headings(html)
        text, tables, code_blocks = extract_utils.extract_content(html, response.url)
        links_out = []
        for href in response.css("a::attr(href)").getall():
            cleaned = strip_tracking(href)
            if not cleaned:
                continue
            abs_url = urljoin(response.url, cleaned)
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
            "source": self.name,
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