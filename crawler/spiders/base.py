from abc import ABC
import urllib.parse as urlparse
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

    def get_next_page(self, url, page_params="page"):
        parsed = urlparse.urlparse(url)
        query_dict = urlparse.parse_qs(parsed.query)
        if page_params in query_dict:
            next_page_number = int(query_dict[page_params][0]) + 1
            if next_page_number > 100:
                return
            query_dict[page_params] = str(next_page_number)
        else:
            query_dict[page_params] = ["2"]
        return urlparse.urlunparse(
            parsed._replace(query=urlparse.urlencode(query_dict, doseq=True))
        )

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

