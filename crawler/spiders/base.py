from abc import ABC
import scrapy

class BaseSpider(ABC, scrapy.Spider):
    user_google_cache = False
    name = "base"
    allowed_domains = []
    custom_settings = {
        # "DOWNLOADER_MIDDLEWARES": {
        #     'crawler.middlewares.SeleniumMiddleware': 900
        # },
        "ITEM_PIPELINES": {
            'crawler.pipelines.CsvPipeline': 300,
        },
        # "HTTPCACHE_ENABLED": True,
        # "HTTPCACHE_EXPIRATION_SECS": 0,
        # "HTTPCACHE_DIR": "httpcache",
        # "HTTPCACHE_IGNORE_HTTP_CODES": [],
        # "HTTPCACHE_STORAGE": "scrapy.extensions.httpcache.FilesystemCacheStorage"
    }

    def start_requests(self):
        pass

    def parse(self, response):
        pass

    def request(self, **kwargs):
        return scrapy.Request(**kwargs)

    def google_cache_request(self, **kwargs):
        if not self.user_google_cache:
            raise Exception('You must set user_google_cache to True in your spider')
        return scrapy.Request(
            **kwargs,
            url=f'http://webcache.googleusercontent.com/search?q=cache:{kwargs["url"]}',
            headers={'Cache-Control': 'no-cache'}
        )

    def tor_request(self, **kwargs):
        proxy = "http://privoxy:8118"
        meta = kwargs.pop('meta', {})
        meta['proxy'] = proxy
        return scrapy.Request(
            **kwargs,
            meta=meta
        )

