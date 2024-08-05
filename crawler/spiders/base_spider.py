import datetime
from abc import ABC
import urllib.parse as urlparse
import scrapy
from scrapy_playwright.page import PageMethod


class BaseSpider(ABC, scrapy.Spider):
    user_google_cache = False
    name = "base"
    allowed_domains = []
    custom_settings = {
        "ITEM_PIPELINES": {
            'crawler.pipelines.CsvPipeline': 300,
        },
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

    def playwright_request(self, **kwargs):
        kwargs.setdefault('meta', {}).update({
            "playwright": True,
            "playwright_page_goto_kwargs": {
                "wait_until": "networkidle",
                "timeout": 20 * 1000
            },
            "playwright_page_methods": [
                PageMethod("screenshot", path=f"/logs/screenshots/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png", full_page=True),
            ],
        })
        return self.request(**kwargs)

    def tor_request(self, **kwargs):
        proxy = "http://privoxy:8118"
        meta = kwargs.pop('meta', {})
        meta['proxy'] = proxy
        return self.request(
            **kwargs,
            meta=meta
        )

