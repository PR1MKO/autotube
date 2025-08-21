# Excel Crawler

This project crawls Microsoft Excel help content from official Microsoft Support and Learn websites in both English (en-us) and Hungarian (hu-hu).

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
scrapy crawl support_excel
scrapy crawl learn_excel
