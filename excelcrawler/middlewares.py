import time


class RetryAfterMiddleware:
    """Simple middleware honoring Retry-After header on 429/503 responses."""

    def process_response(self, request, response, spider):
        if response.status in (429, 503):
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = int(retry_after.decode())
                    spider.logger.info("Retry-After %s sec for %s", delay, request.url)
                    time.sleep(delay)
                except ValueError:
                    pass
            return request
        return response