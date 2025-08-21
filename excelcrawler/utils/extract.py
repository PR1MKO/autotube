import json
from bs4 import BeautifulSoup
from readability import Document
import trafilatura


def _extract_trafilatura(html: str, url: str):
    result = trafilatura.extract(
        html,
        url=url,
        favor_precision=True,
        include_links=False,
        include_tables=True,
        output_format="json",
    )
    if not result:
        return None
    data = json.loads(result)
    text = data.get("text") or ""
    tables = [
        {"markdown": t, "caption": ""} for t in data.get("tables", [])
    ]
    return text, tables


def _table_to_md(table):
    rows = []
    for tr in table.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
        rows.append("|" + "|".join(cells) + "|")
    markdown = "\n".join(rows)
    caption = ""
    cap = table.find("caption")
    if cap:
        caption = cap.get_text(strip=True)
    return markdown, caption


def _html_to_md(html: str):
    soup = BeautifulSoup(html, "lxml")
    parts = []
    tables = []
    for el in soup.find_all(["p", "h1", "h2", "h3", "ul", "ol", "pre", "table"]):
        if el.name in ["p", "h1", "h2", "h3"]:
            parts.append(el.get_text(" ", strip=True))
        elif el.name in ["ul", "ol"]:
            for li in el.find_all("li"):
                parts.append("* " + li.get_text(" ", strip=True))
        elif el.name == "pre":
            parts.append("```\n" + el.get_text("\n", strip=True) + "\n```")
        elif el.name == "table":
            md, caption = _table_to_md(el)
            tables.append({"markdown": md, "caption": caption})
            parts.append(md)
    return "\n\n".join(parts), tables


def extract_content(html: str, url: str):
    res = _extract_trafilatura(html, url)
    if res:
        text, tables = res
    else:
        doc = Document(html)
        text, tables = _html_to_md(doc.summary())
    soup = BeautifulSoup(html, "lxml")
    code_blocks = []
    for code in soup.find_all("code"):
        code_text = code.get_text("\n", strip=True)
        if code_text:
            code_blocks.append({"language": "excel", "text": code_text})
    for line in text.splitlines():
        if line.strip().startswith("="):
            code_blocks.append({"language": "excel", "text": line.strip()})
    return text, tables, code_blocks