from scrapy.crawler import CrawlerProcess

from crawler.spiders.base import BaseSpider

if __name__ == '__main__':
    process = CrawlerProcess()
    # process.crawl(BaseSpider)
    process.start()  # the script will block here until all crawling jobs are finished
