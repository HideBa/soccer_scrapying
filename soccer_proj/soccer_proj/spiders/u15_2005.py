# -*- coding: utf-8 -*-
import scrapy
import pprint
from ..items import SoccerProjItem
from ..selenium_middleware import *
import re


u15_game_url_nums = 0
u15_game_url_exist = 0
u15_game_url_no_exist = 0


class U152005Spider(scrapy.Spider):
    name = 'u15_2005'
    allowed_domains = [
        'http://www.jfa.or.jp/archive/domestic/category_3/games/2005/takamado_jy_2005/']
    start_urls = [
        'http://http://www.jfa.or.jp/archive/domestic/category_3/games/2005/takamado_jy_2005//']
    custom_setting = {
        "DOWNLOAD_MIDDLEWARE": {
            "scrapy_list.selenium_middleware.ScrapyListSpiderMiddleware"
        },
        "DOWNLOAD_DELAY": 5.0,
    }

    def start_requests(self):
        url = 'http://www.jfa.or.jp/archive/domestic/category_3/games/2005/takamado_jy_2005/'

        selenium_get(url)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        datas = response.css(
            'div.repCntAreaBack > div > div > table:nth-child(8) tr')
        print("datas_len " + str(len(datas)))
        for data in datas:
            # print("data =========- " + str(data.css('::text')))
            year = data.css('td:nth-child(1) span::text').extract_first()
            print('year=============' + str(year))
            if re.search("[0-9]", str(year)):
                item = SoccerProjItem()
                year = '20' + re.search('[0-9]+', year).group()
                item['year'] = year
            else:
                continue

            team_home = data.css(
                'tr > td:nth-child(3) > span::text').extract_first()
            team_away = data.css(
                'tr td:nth-child(5) > span::text').extract_first()
            item['team_home'] = team_home
            item['team_away'] = team_away
            month = data.css('td:nth-child(1) span::text').extract_first()
            month = month[3:5]
            item['month'] = month
            day = data.css('td:nth-child(1) span::text').extract_first()
            day = day[6:8]
            item['day'] = day


# td: nth-child(4) > span > a
# table:nth-child(8) > tbody > tr:nth-child(3) > td:nth-child(4) > div > a
            result = data.css(
                'td:nth-child(4) > span a::text').extract()
            if result:
                result = result[0].strip()
                url = data.css(
                    "td:nth-child(4) > span a::attr(href)").extract_first()
                url = response.urljoin(url)
                item['url'] = url
                if item['url']:
                    self.add_url_no_exist_nums(1)
                item['results_home'] = re.search('[0-9]+', result).group()
                item['results_away'] = re.search(
                    '\-[0-9]+', result).group().replace("-", "")
            if not result:
                result = data.css('td:nth-child(4) > div > a::text').extract()
                result = list(map(lambda x: x.strip(), result))
                url = data.css(
                    "td:nth-child(4) > div > a::attr(href)").extract_first()
                url = response.urljoin(url)
                item['url'] = url
                if item['url']:
                    self.add_url_no_exist_nums(1)
                print("result============" + str(result))
                item['results_home'] = re.search('[0-9]+', result[1]).group()
                item['results_away'] = re.search(
                    'PK[0-9]+', result[1]).group().replace("PK", "")

            item['leagu_name'] = "高円宮杯全日本ユース(U-15)サッカー選手権大会"
            yield item

    def add_url_nums(self, urls):
        global u15_game_url_nums
        u15_game_url_nums += urls

    def add_url_exist_nums(self, url):
        global u15_game_url_exist
        u15_game_url_exist += url

    def add_url_no_exist_nums(self, url):
        global u15_game_url_no_exist
        u15_game_url_no_exist += url

    def get_url_rate(self, game_url, game_url_exist):
        return game_url_exist/game_url

    def get_no_url_nums(self):
        return u15_game_url_no_exist

    def closed(self, response):
        selenium_close()
