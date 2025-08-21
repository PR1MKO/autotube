<<<<<<< HEAD
autotube
=======
# Excel Crawler

This project crawls Microsoft Excel help content from official Microsoft Support and Learn websites in both English (en-us) and Hungarian (hu-hu).

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
scrapy crawl support_excel
scrapy crawl learn_excel
```

## Outputs
- Raw HTML: `data/pages_raw/<slug>.html`
- Extracted data (JSONL): `data/pages_jsonl/<spider>.jsonl`
- HTTP cache for incremental recrawls: `data/cache/`

Each JSON line contains the page metadata, cleaned text, tables, code blocks and outbound links.

## Politeness
The spiders obey `robots.txt`, throttle requests, respect `Retry-After` headers on 429/503 responses and use an explicit user agent.

## Incremental Recrawls
HTTPCACHE is enabled by default. To re-crawl incrementally, simply run the spiders again. Scrapy will issue conditional requests using ETag/Last-Modified when available, reducing bandwidth and server load.

## Coverage Report
After running the spiders, you can generate a basic coverage report:

```bash
python tools/coverage_report.py data/pages_jsonl/support_excel.jsonl data/pages_jsonl/learn_excel.jsonl
```

## Known limits / TODO
- Some dynamic or script-heavy pages may not extract perfectly without a headless browser.
- Embedded media and complex widgets are not captured.
- Table and formula extraction is best-effort and may miss edge cases.
>>>>>>> 787029e (✨ Initial commit: Excel crawler (support + learn spiders))
