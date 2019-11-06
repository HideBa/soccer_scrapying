# -*- coding: utf-8 -*-
import scrapy
import pprint
from ..items import SoccerProjItem
from ..selenium_middleware import *
import re


class U152006Spider(scrapy.Spider):
    name = 'u15_2006'
    allowed_domains = [
        'http://www.jfa.or.jp/archive/domestic/category_3/games/2006/takamado_jy_2006/']
    start_urls = [
        'http://http://www.jfa.or.jp/archive/domestic/category_3/games/2006/takamado_jy_2006//']
    custom_setting = {
        "DOWNLOAD_MIDDLEWARE": {
            "scrapy_list.selenium_middleware.ScrapyListSpiderMiddleware"
        },
        "DOWNLOAD_DELAY": 5.0,
    }

    def start_requests(self):
        url_list = [
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2006/takamado_jy_2006/result05/index.html",
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2006/takamado_jy_2006/result04/index.html",
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2006/takamado_jy_2006/result03/index.html",
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2006/takamado_jy_2006/result02/index.html",
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2006/takamado_jy_2006/result01/index.html"
        ]

        for url in url_list:
            # if any((s in url) for s in ['2007']):

            if 'result05' in url:
                selenium_get(url)
                yield scrapy.Request(url, callback=self.parse_round_1)

            elif 'result04' in url:
                selenium_get(url)
                yield scrapy.Request(url, callback=self.parse_round_1)
            elif 'result03' in url:
                selenium_get(url)
                yield scrapy.Request(url, callback=self.parse_round_2)
            elif 'result02' in url:
                selenium_get(url)
                yield scrapy.Request(url, callback=self.parse_round_2)
            elif 'result01' in url:
                selenium_get(url)
                yield scrapy.Request(url, callback=self.parse_round_1)
            #     elif 'round_3' in url:
            #         selenium_get(url)
            #         yield scrapy.Request(url, callback=self.parse_round_1)
            #     elif 'round_4' in url:
            #         selenium_get(url)
            #         yield scrapy.Request(url, callback=self.parse_round_1)
            #     else:
            #         selenium_get(url)
            #         yield scrapy.Request(url, callback=self.parse_final)

    def parse_round_1(self, response):
        # div.repCntAreaBack > div > div > table tr:nth-child(1)
        datas = response.css(
            'div.repCntAreaBack > div > div > table tr')
        for data in datas:
            print("data=================" + str(data.css("::text")))
#  td:nth-child(1) > span
            year = data.css('td:nth-child(1) span::text').extract_first()
            result = data.css('td:nth-child(3) span a::text').extract()
            print("year===" + str(year))
            if re.search("[0-9]", str(year)):
                #     if '-' in result[0]:
                item = SoccerProjItem()
                year = '20' + re.search('[0-9]+', year).group()
                item['year'] = year
            else:
                continue
            # else:
            #     continue
            team_home = data.css(
                'td:nth-child(2) span::text').extract_first()
            team_away = data.css(
                'td:nth-child(4) span::text').extract_first()
            item['team_home'] = team_home
            item['team_away'] = team_away
            month = data.css('td:nth-child(1) span::text').extract_first()
            month = month[3:5]
            item['month'] = month
            day = data.css('td:nth-child(1) span::text').extract_first()
            day = day[6:8]
            item['day'] = day
            result = data.css('td:nth-child(3) span a::text').extract()
            print("result============" + str(result))
            item['results_home'] = re.search('[0-9]+', result[0]).group()
            item['results_away'] = re.search(
                '\-[0-9]+', result[0]).group().replace("-", "")
            # item['id'] = data.css('td:nth-child(1)::text').extract_first()
            url = data.css(
                "td:nth-child(3) span a::attr(href)").extract_first()
            url = response.urljoin(url)
            item['url'] = url
            # if item['url']:
            #     self.add_url_no_exist_nums(1)
            # print("no url_nums ==== " + str(self.get_no_url_nums()))
            item['leagu_name'] = "高円宮杯 第18回全日本ユース（U-15）サッカー選手権大会"
            yield item

    def parse_round_2(self, response):
        # div.repCntAreaBack > div > div > table tr:nth-child(1)
        datas = response.css(
            'div.repCntAreaBack > div > div > table tr')
        for data in datas:
            print("data=================" + str(data.css("::text")))
#  td:nth-child(1) > span
            year = data.css('td:nth-child(1) span::text').extract_first()
            result = data.css('td:nth-child(4) span a::text').extract()
            print("year===" + str(year))
            if re.search("[0-9]", str(year)):
                #     if '-' in result[0]:
                item = SoccerProjItem()
                year = '20' + re.search('[0-9]+', year).group()
                item['year'] = year
            else:
                continue
            # else:
            #     continue
            team_home = data.css(
                'td:nth-child(3) span::text').extract_first()
            team_away = data.css(
                'td:nth-child(5) span::text').extract_first()
            item['team_home'] = team_home
            item['team_away'] = team_away
            month = data.css('td:nth-child(1) span::text').extract_first()
            month = month[3:5]
            item['month'] = month
            day = data.css('td:nth-child(1) span::text').extract_first()
            day = day[6:8]
            item['day'] = day
            result = data.css('td:nth-child(4) span a::text').extract()
            print("result============" + str(result))
            item['results_home'] = re.search('[0-9]+', result[0]).group()
            item['results_away'] = re.search(
                '\-[0-9]+', result[0]).group().replace("-", "")
            # item['id'] = data.css('td:nth-child(1)::text').extract_first()
            url = data.css(
                "td:nth-child(4) span a::attr(href)").extract_first()
            url = response.urljoin(url)
            item['url'] = url
            # if item['url']:
            #     self.add_url_no_exist_nums(1)
            # print("no url_nums ==== " + str(self.get_no_url_nums()))
            item['leagu_name'] = "高円宮杯 第18回全日本ユース（U-15）サッカー選手権大会"
            yield item

    def closed(self, response):
        selenium_close()

    # def parse(self, response):
    #     pass
