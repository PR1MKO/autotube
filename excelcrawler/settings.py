import os

BOT_NAME = "excelcrawler"

SPIDER_MODULES = ["excelcrawler.spiders"]
NEWSPIDER_MODULE = "excelcrawler.spiders"

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 0.7
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = "data/cache"
RETRY_ENABLED = True
RETRY_TIMES = 3
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "ExcelKBBot/0.1 (research; contact: youremail@example.com)",
    "Accept-Language": "en-US,en;q=0.8,hu-HU;q=0.6",
}
FEED_EXPORT_ENCODING = "utf-8"
LOG_LEVEL = "INFO"

ITEM_PIPELINES = {
    "excelcrawler.pipelines.JsonlWriterPipeline": 300,
}

DOWNLOADER_MIDDLEWARES = {
    "excelcrawler.middlewares.RetryAfterMiddleware": 100,
}