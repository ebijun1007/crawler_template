from abc import ABC, abstractmethod
import scrapy

class BaseSpider(ABC, scrapy.Spider):
    user_google_cache = False
    @abstractmethod

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_domains.append('webcache.googleusercontent.com')

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

