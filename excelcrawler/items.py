import scrapy


class PageItem(scrapy.Item):
    url = scrapy.Field()
    canonical_url = scrapy.Field()
    locale = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    breadcrumbs = scrapy.Field()
    headings = scrapy.Field()
    text_md = scrapy.Field()
    code_blocks = scrapy.Field()
    tables = scrapy.Field()
    links_out = scrapy.Field()
    last_modified = scrapy.Field()
    etag = scrapy.Field()
    html_path = scrapy.Field()
    sha256 = scrapy.Field()
    fetched_at = scrapy.Field()