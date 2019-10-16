# -*- coding: utf-8 -*-
# import os.path

# from urllib.parse import urlparse

# import arrow

from scrapy.http import HtmlResponse
# from selenium.webdriver import Firefox
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# options = Options()

# # ヘッドレスにするには必須
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')

# # 必須じゃないけどUserAgentとか変更したいなら追加する
# options.add_argument('--lang=ja')
# options.add_argument(
#     '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')

# Chromeを指定。ここでFireFoxなども指定できるがHeadlessはないかも。
# try:
#     driver = webdriver.Chrome(chrome_options=options)
#     driver.get(
#         'http://www.jfa.jp/match/takamado_jfa_u18_premier2019/east/schedule_result/')
# except:
#     print('error')
#     pass
# finally:
#     driver.quit()

# Chromeで任意のサイトを開く

driver = webdriver.Chrome()


def selenium_get(url):
    driver.get(url)


def get_a(query):
    alist = driver.find_elements_by_css_selector(query)
    print(str(type(alist)))
    return alist


def get_dom(query):
    dom = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, query)))
    return dom

# Chromeを閉じる


def selenium_close():
    driver.close()

# こちらがミドルウェア本体


class ScrapyListSpiderMiddleware(object):
    def process_request(self, request, spider):
        driver.get(request.url)
        return HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request)

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# Chromeの場合
# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Chrome(executable_path="D:\各種インストーラー\chromedriver_win32", chrome_options=options)
# ==============

# driver = webdriver.Firefox()

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_selenium.SeleniumMiddleware': 800
# }

# Firefoxの場合
# driver = Firefox()
# driver = webdriver.Firefox(executable_path='geckodriver')
# driver.get('http://www.jfa.jp/match/takamado_jfa_u18_premier2019/east/schedule_result/')


class SeleniumMiddleware(object):

    def process_request(self, request, spider):

        driver.get(request.url)

        return HtmlResponse(driver.current_url,
                            body=driver.page_source,
                            encoding='utf-8',
                            request=request)


def close_driver():
    driver.close()
