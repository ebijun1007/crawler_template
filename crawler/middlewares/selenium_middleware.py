import logging
import time
from scrapy import signals

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException


class SeleniumMiddleware:
    def __init__(self):
        self.driver = self._initialize_driver()

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.INFO)
        return middleware

    def process_request(self, request, spider):
        try:
            self.driver.get(request.url)
        except InvalidSessionIdException:
            self.driver = self._initialize_driver()  # ここで新しいdriverを初期化
            self.driver.get(request.url)
        try:
            by, value = request.meta["wait_for"]
            WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((by, value)))  # wait until an HTML tag is present
        except:
            time.sleep(10)
        url = self.driver.current_url
        body = self.driver.page_source
        if "screenshot" in request.meta:
            filename = request.meta["screenshot"] + ".png"
            self.driver.save_screenshot(filename)
        if self.driver.current_url != 'about:blank':
            self.driver.get('about:blank')
        return HtmlResponse(url=url, body=body, encoding='utf-8', request=request)

    def spider_closed(self):
        self.driver.quit()

    def _initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Remote(
            command_executor='http://browser:4444/wd/hub',
            options=chrome_options
        )
        driver.maximize_window()
        return driver
