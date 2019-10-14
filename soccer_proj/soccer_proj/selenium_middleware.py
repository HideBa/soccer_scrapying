# -*- coding: utf-8 -*-
import os.path

from urllib.parse import urlparse

import arrow

from scrapy.http import HtmlResponse
from selenium.webdriver import Firefox


driver = Firefox()


class SeleniumMiddleware(object):

    def process_request(self, request, spider):

        driver.get(request.url)

        return HtmlResponse(driver.current_url,
                            body=driver.page_source,
                            encoding='utf-8',
                            request=request)


def close_driver():
    driver.close()
