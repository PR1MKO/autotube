import os

BOT_NAME = "excelcrawler"

SPIDER_MODULES = ["excelcrawler.spiders"]
NEWSPIDER_MODULE = "excelcrawler.spiders"

# Politeness
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 0.35

# Parallelism
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# AutoThrottle (adaptive politeness)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 8.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Caching
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = "data/cache"

# Retries
RETRY_ENABLED = True
RETRY_TIMES = 3

# Default headers
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "ExcelKBBot/0.1 (research; contact: youremail@example.com)",
    "Accept-Language": "en-US,en;q=0.8,hu-HU;q=0.6",
}

# Output & logging
FEED_EXPORT_ENCODING = "utf-8"
LOG_LEVEL = "INFO"

# Pipelines
ITEM_PIPELINES = {
    "excelcrawler.pipelines.JsonlWriterPipeline": 300,
}

# Middlewares
DOWNLOADER_MIDDLEWARES = {
    "excelcrawler.middlewares.RetryAfterMiddleware": 100,
}

# Depth & stop conditions
# (Important: ensure CLOSESPIDER_PAGECOUNT is not set anywhere to non-zero)
# DEPTH_LIMIT provides a safety ceiling without premature stop
DEPTH_LIMIT = 6

# Resume support (safe to keep; Scrapy will create the folder)
JOBDIR = "data/state/learn_excel"
