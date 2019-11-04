# -*- coding: utf-8 -*-
import scrapy
import pprint
from ..items import SoccerProjItem
from ..selenium_middleware import *
import re

u15_game_url_nums = 0
u15_game_url_exist = 0
u15_game_url_no_exist = 0


class U152007Spider(scrapy.Spider):
    name = 'u15_2007'
    allowed_domains = [
        'http://www.jfa.or.jp/archive/domestic/category_3/games/2007/takamado_jy_2007/round_f.html#5th']
    start_urls = [
        'http://http://www.jfa.or.jp/archive/domestic/category_3/games/2007/takamado_jy_2007/round_f.html#5th/']
    custom_setting = {
        "DOWNLOAD_MIDDLEWARE": {
            "scrapy_list.selenium_middleware.ScrapyListSpiderMiddleware"
        },
        "DOWNLOAD_DELAY": 5.0,
    }

    def start_requests(self):
        url_list = [
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2007/takamado_jy_2007/",
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2007/takamado_jy_2007/round_1.html",
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2007/takamado_jy_2007/round_2.html",
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2007/takamado_jy_2007/round_3.html",
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2007/takamado_jy_2007/round_4.html",
        ]
        for url in url_list:
            if any((s in url) for s in ['2007']):

                if 'round_1' in url:
                    selenium_get(url)
                    yield scrapy.Request(url, callback=self.parse_round_1)

                elif 'round_2' in url:
                    selenium_get(url)
                    yield scrapy.Request(url, callback=self.parse_round_1)
                elif 'round_3' in url:
                    selenium_get(url)
                    yield scrapy.Request(url, callback=self.parse_round_1)
                elif 'round_4' in url:
                    selenium_get(url)
                    yield scrapy.Request(url, callback=self.parse_round_1)
                else:
                    selenium_get(url)
                    yield scrapy.Request(url, callback=self.parse_final)

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
# menuList1 > table:nth-child(1) > tbody > tr:nth-child(2)
# menuList1 > table:nth-child(1) > tbody > tr:nth-child(3)

    def parse_round_1(self, response):
        datas = response.css('#menuList1 > table tr')
        for data in datas:
            print("data=================" + str(data.css("::text")))
            year = data.css('td:nth-child(2)::text').extract_first()
            result = data.css('td:nth-child(6)::text').extract()
            # print("year===" + year)
            if re.search("[0-9]", str(year)):
                if '-' in result[0]:
                    item = SoccerProjItem()
                    year = '20' + re.search('[0-9]+', year).group()
                    item['year'] = year
                else:
                    continue
            else:
                continue
            team_home = data.css(
                'td:nth-child(5) td:nth-child(1)::text').extract_first()
            team_away = data.css(
                'td:nth-child(5) td:nth-child(3)::text').extract_first()
            item['team_home'] = team_home
            item['team_away'] = team_away
            month = data.css('td:nth-child(2)::text').extract_first()
            month = month[3:5]
            item['month'] = month
            day = data.css('td:nth-child(2)::text').extract_first()
            day = day[6:8]
            item['day'] = day
            result = data.css('td:nth-child(6)::text').extract()
            print("result============" + str(result))
            item['results_home'] = re.search('[0-9]+', result[0]).group()
            item['results_away'] = re.search(
                '\-[0-9]+', result[0]).group().replace("-", "")
            item['id'] = data.css('td:nth-child(1)::text').extract_first()
            url = data.css("td:nth-child(7) a::attr(href)").extract_first()
            url = response.urljoin(url)
            item['url'] = url
            if item['url']:
                self.add_url_no_exist_nums(1)
            print("no url_nums ==== " + str(self.get_no_url_nums()))
            item['leagu_name'] = "高円宮杯 第19回全日本ユース（U-15）サッカー選手権大会"
            yield item

        item = SoccerProjItem()
        year = response.css(
            '#menuList1 > table > td:nth-child(4)::text').extract()[0]
        year = '20' + re.search('[0-9]+', year).group()
        item['year'] = year
        team_home = response.css(
            '#menuList1 > table > td:nth-child(7) td:nth-child(1)::text').extract()[0]
        team_away = response.css(
            '#menuList1 > table > td:nth-child(7) td:nth-child(3)::text').extract()[0]
        item['team_home'] = team_home
        item['team_away'] = team_away
        month = response.css(
            '#menuList1 > table > td:nth-child(4)::text').extract()[0]
        month = month[3:5]
        item['month'] = month
        day = response.css(
            '#menuList1 > table > td:nth-child(4)::text').extract()[0]
        day = day[6:8]
        item['day'] = day
        result = response.css(
            '#menuList1 > table > td:nth-child(8)::text').extract()[0]
        print("result============" + str(result))
        item['results_home'] = re.search('[0-9]+', result).group()
        item['results_away'] = re.search(
            '\-[0-9]+', result).group().replace("-", "")
        item['id'] = response.css(
            '#menuList1 > table > td:nth-child(3)::text').extract()[0]
        url = response.css(
            "#menuList1 > table > td:nth-child(9) a::attr(href)").extract()[0]
        url = response.urljoin(url)
        item['url'] = url
        if item['url']:
            self.add_url_no_exist_nums(1)
        print("no url_nums ==== " + str(self.get_no_url_nums()))
        item['leagu_name'] = "高円宮杯 第19回全日本ユース（U-15）サッカー選手権大会"
        yield item

        item = SoccerProjItem()
        year = response.css(
            '#menuList1 > table > td:nth-child(4)::text').extract()[1]
        year = '20' + re.search('[0-9]+', year).group()
        item['year'] = year
        team_home = response.css(
            '#menuList1 > table > td:nth-child(7) td:nth-child(1)::text').extract()[1]
        team_away = response.css(
            '#menuList1 > table > td:nth-child(7) td:nth-child(3)::text').extract()[1]
        item['team_home'] = team_home
        item['team_away'] = team_away
        month = response.css(
            '#menuList1 > table > td:nth-child(4)::text').extract()[1]
        month = month[3:5]
        item['month'] = month
        day = response.css(
            '#menuList1 > table > td:nth-child(4)::text').extract()[1]
        day = day[6:8]
        item['day'] = day
        result = response.css(
            '#menuList1 > table > td:nth-child(8)::text').extract()[1]
        print("result============" + str(result))
        item['results_home'] = re.search('[0-9]+', result).group()
        item['results_away'] = re.search(
            '\-[0-9]+', result).group().replace("-", "")
        item['id'] = response.css(
            '#menuList1 > table > td:nth-child(3)::text').extract()[1]
        url = response.css(
            "#menuList1 > table > td:nth-child(9) a::attr(href)").extract()[1]
        url = response.urljoin(url)
        item['url'] = url
        if item['url']:
            self.add_url_no_exist_nums(1)
        print("no url_nums ==== " + str(self.get_no_url_nums()))
        item['leagu_name'] = "高円宮杯 第19回全日本ユース（U-15）サッカー選手権大会"
        yield item

    def parse_round_2(self, response):
        datas = response.css('#menuList1 tr')
        for data in datas:
            # print("data=================" + str(data.css("::text")))
            year = data.css('td:nth-child(2)::text').extract_first()
            result = data.css('td:nth-child(6)::text').extract()
            # print("year===" + year)
            if re.search("[0-9]", str(year)):
                if '-' in result[0]:
                    item = SoccerProjItem()
                    year = '20' + re.search('[0-9]+', year).group()
                    item['year'] = year
                else:
                    continue
            else:
                continue
            team_home = data.css(
                'td:nth-child(5) td:nth-child(1)::text').extract_first()
            team_away = data.css(
                'td:nth-child(5) td:nth-child(3)::text').extract_first()
            item['team_home'] = team_home
            item['team_away'] = team_away
            month = data.css('td:nth-child(2)::text').extract_first()
            month = month[3:5]
            item['month'] = month
            day = data.css('td:nth-child(2)::text').extract_first()
            day = day[6:8]
            item['day'] = day
            result = data.css('td:nth-child(6)::text').extract()
            print("result============" + str(result))
            item['results_home'] = re.search('[0-9]+', result[0]).group()
            item['results_away'] = re.search(
                '\-[0-9]+', result[0]).group().replace("-", "")
            item['id'] = data.css('td:nth-child(1)::text').extract_first()
            url = data.css("td:nth-child(7) a::attr(href)").extract_first()
            url = response.urljoin(url)
            item['url'] = url
            if item['url']:
                self.add_url_no_exist_nums(1)
            print("no url_nums ==== " + str(self.get_no_url_nums()))
            yield item

    def parse_round_3(self, response):
        datas = response.css('#menuList1 tr')
        for data in datas:
            # print("data=================" + str(data.css("::text")))
            year = data.css('td:nth-child(2)::text').extract_first()
            result = data.css('td:nth-child(6)::text').extract()
            # print("year===" + year)
            if re.search("[0-9]", str(year)):
                if '-' in result[0]:
                    item = SoccerProjItem()
                    year = '20' + re.search('[0-9]+', year).group()
                    item['year'] = year
                else:
                    continue
            else:
                continue
            team_home = data.css(
                'td:nth-child(5) td:nth-child(1)::text').extract_first()
            team_away = data.css(
                'td:nth-child(5) td:nth-child(3)::text').extract_first()
            item['team_home'] = team_home
            item['team_away'] = team_away
            month = data.css('td:nth-child(2)::text').extract_first()
            month = month[3:5]
            item['month'] = month
            day = data.css('td:nth-child(2)::text').extract_first()
            day = day[6:8]
            item['day'] = day
            result = data.css('td:nth-child(6)::text').extract()
            print("result============" + str(result))
            item['results_home'] = re.search('[0-9]+', result[0]).group()
            item['results_away'] = re.search(
                '\-[0-9]+', result[0]).group().replace("-", "")
            item['id'] = data.css('td:nth-child(1)::text').extract_first()
            url = data.css("td:nth-child(7) a::attr(href)").extract_first()
            url = response.urljoin(url)
            item['url'] = url
            if item['url']:
                self.add_url_no_exist_nums(1)
            print("no url_nums ==== " + str(self.get_no_url_nums()))
            yield item

    def parse_round_4(self, response):
        datas = response.css('#menuList1 tr')
        for data in datas:
            # print("data=================" + str(data.css("::text")))
            year = data.css('td:nth-child(2)::text').extract_first()
            result = data.css('td:nth-child(6)::text').extract()
            # print("year===" + year)
            if re.search("[0-9]", str(year)):
                if '-' in result[0]:
                    item = SoccerProjItem()
                    year = '20' + re.search('[0-9]+', year).group()
                    item['year'] = year
                else:
                    continue
            else:
                continue
            team_home = data.css(
                'td:nth-child(5) td:nth-child(1)::text').extract_first()
            team_away = data.css(
                'td:nth-child(5) td:nth-child(3)::text').extract_first()
            item['team_home'] = team_home
            item['team_away'] = team_away
            month = data.css('td:nth-child(2)::text').extract_first()
            month = month[3:5]
            item['month'] = month
            day = data.css('td:nth-child(2)::text').extract_first()
            day = day[6:8]
            item['day'] = day
            result = data.css('td:nth-child(6)::text').extract()
            print("result============" + str(result))
            item['results_home'] = re.search('[0-9]+', result[0]).group()
            item['results_away'] = re.search(
                '\-[0-9]+', result[0]).group().replace("-", "")
            item['id'] = data.css('td:nth-child(1)::text').extract_first()
            url = data.css("td:nth-child(7) a::attr(href)").extract_first()
            url = response.urljoin(url)
            item['url'] = url
            if item['url']:
                self.add_url_no_exist_nums(1)
            print("no url_nums ==== " + str(self.get_no_url_nums()))
            yield item

    def parse_final(self, response):
        datas = response.css(
            'div.repCntAreaBack > div > div table:nth-child(14) tr')
        for data in datas:
            year = data.css('td:nth-child(2)::text').extract_first()
            if re.search("[0-9]", str(year)):
                item = SoccerProjItem()
                year = '20' + re.search('[0-9]+', year).group()
                item['year'] = year
            else:
                continue
            team_home = data.css(
                'td:nth-child(5) td:nth-child(1)::text').extract_first()
            team_away = data.css(
                'td:nth-child(5) td:nth-child(3)::text').extract_first()
            item['team_home'] = team_home
            item['team_away'] = team_away
            month = data.css('td:nth-child(2)::text').extract_first()
            month = month[3:5]
            item['month'] = month
            day = data.css('td:nth-child(2)::text').extract_first()
            day = day[6:8]
            item['day'] = day
            result = data.css('td:nth-child(6)::text').extract()
            item['results_home'] = re.search('[0-9]+', result[0]).group()
            item['results_away'] = re.search(
                '\-[0-9]+', result[0]).group().replace("-", "")
            item['id'] = data.css('td:nth-child(1)::text').extract_first()
            url = data.css("td:nth-child(7) a::attr(href)").extract_first()
            url = response.urljoin(url)
            item['url'] = url
            if item['url']:
                self.add_url_no_exist_nums(1)
            print("no url_nums ==== " + str(self.get_no_url_nums()))
            item['leagu_name'] = "高円宮杯 第19回全日本ユース（U-15）サッカー選手権大会"
            yield item

        datas2 = response.css(
            'div.repCntAreaBack > div > div table:nth-child(18) tr')
        for data in datas2:
            year = data.css('td:nth-child(2)::text').extract_first()
            if re.search("[0-9]", str(year)):
                item = SoccerProjItem()
                year = '20' + re.search('[0-9]+', year).group()
                item['year'] = year
            else:
                continue
            team_home = data.css(
                'td:nth-child(5) td:nth-child(1)::text').extract_first()
            team_away = data.css(
                'td:nth-child(5) td:nth-child(3)::text').extract_first()

            item['team_home'] = team_home
            item['team_away'] = team_away
            month = data.css('td:nth-child(2)::text').extract_first()
            month = month[3:5]
            item['month'] = month
            day = data.css('td:nth-child(2)::text').extract_first()
            day = day[6:8]
            item['day'] = day
            result = data.css('td:nth-child(6)::text').extract()
            item['results_home'] = re.search('[0-9]+', result[0]).group()
            item['results_away'] = re.search(
                '\-[0-9]+', result[0]).group().replace("-", "")
            item['id'] = data.css('td:nth-child(1)::text').extract_first()
            url = data.css("td:nth-child(7) a::attr(href)").extract_first()
            url = response.urljoin(url)
            item['url'] = url
            if item['url']:
                self.add_url_no_exist_nums(1)
            print("no url_nums ==== " + str(self.get_no_url_nums()))
            item['leagu_name'] = "高円宮杯 第19回全日本ユース（U-15）サッカー選手権大会"
            yield item
# table:nth-child(23) > tbody > tr:nth-child(2) > td:nth-child(6) > a
        # datas3 = response.css(
        #     'div.repCntAreaBack > div > div table:nth-child(23) tr')
        # for data in datas3:
        #     year = data.css('td:nth-child(2)::text').extract_first()
        #     if re.search("[0-9]", str(year)):
        #         item = SoccerProjItem()
        #         year = '20' + re.search('[0-9]+', year).group()
        #         item['year'] = year
        #     else:
        #         continue
        #     team_home = data.css(
        #         'td:nth-child(5) td:nth-child(1)::text').extract_first()
        #     team_away = data.css(
        #         'td:nth-child(5) td:nth-child(3)::text').extract_first()
        #     item['team_home'] = team_home
        #     item['team_away'] = team_away
        #     month = data.css('td:nth-child(2)::text').extract_first()
        #     month = re.search('..\.[0-9]+', month).group()
        #     date = data.css('td:nth-child(2)::text').extract_first()
        #     date = re.search('..\...\.[0-9]+', date).group()
        #     item['day'] = re.sub('../../', '', date)
        #     result = data.css('td:nth-child(6) a::text').extract()
        #     item['results_home'] = re.search('[0-9]+', result[0]).group()
        #     item['results_away'] = re.search(
        #         '\-[0-9]+', result[0]).group().replace("-", "")
        #     url = data.css("td:nth-child(7) a::attr(href)").extract_first()
        #     url = response.urljoin(url)
        #     item['url'] = url
        #     yield item

        # datas4 = response.css(
        #     'div.repCntAreaBack > div > div table:nth-child(28) tr')
        # for data in datas4:
        #     year = data.css('td:nth-child(2)::text').extract_first()
        #     if re.search("[0-9]", str(year)):
        #         item = SoccerProjItem()
        #         year = '20' + re.search('[0-9]+', year).group()
        #         item['year'] = year
        #     else:
        #         continue
        #     team_home = data.css(
        #         'td:nth-child(5) td:nth-child(1)::text').extract_first()
        #     team_away = data.css(
        #         'td:nth-child(5) td:nth-child(3)::text').extract_first()
        #     item['team_home'] = team_home
        #     item['team_away'] = team_away
        #     month = data.css('td:nth-child(2)::text').extract_first()
        #     month = re.search('..\.[0-9]+', month).group()
        #     date = data.css('td:nth-child(2)::text').extract_first()
        #     date = re.search('..\...\.[0-9]+', date).group()
        #     item['day'] = re.sub('../../', '', date)
        #     result = data.css('td:nth-child(6) a::text').extract()
        #     item['results_home'] = re.search('[0-9]+', result[0]).group()
        #     item['results_away'] = re.search(
        #         '\-[0-9]+', result[0]).group().replace("-", "")
        #     # print("results ======== " + str(result_home))
        #     url = data.css("td:nth-child(7) a::attr(href)").extract_first()
        #     url = response.urljoin(url)
        #     item['url'] = url
        #     yield item

    def closed(self, response):
        selenium_close()
