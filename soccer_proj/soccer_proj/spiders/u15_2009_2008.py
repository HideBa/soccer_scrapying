
# -*- coding: utf-8 -*-
import scrapy
import pprint
from ..items import SoccerProjItem
from ..selenium_middleware import *
import re


u15_game_url_nums = 0
u15_game_url_exist = 0


class U1520092008Spider(scrapy.Spider):
    name = 'u15_2009_2008'
    allowed_domains = [
        'http://www.jfa.or.jp/match/matches/2009/takamado_u15/schedule_result/schedule.html']
    start_urls = [
        'http://http://www.jfa.or.jp/match/matches/2009/takamado_u15/schedule_result/schedule.html/']

    custom_setting = {
        "DOWNLOAD_MIDDLEWARE": {
            "scrapy_list.selenium_middleware.ScrapyListSpiderMiddleware"
        },
        "DOWNLOAD_DELAY": 5.0,
    }

    def start_requests(self):
        url_list = [
            "http://www.jfa.or.jp/match/matches/2009/takamado_u15/schedule_result/schedule.html",
            "http://www.jfa.or.jp/match/matches/2008/takamado_u15/schedule_result/schedule.html",
        ]
        # ----------------------------------2009年以前はそもそも各試合の詳細ページが存在しない。－－－－－－－－－－

        for url in url_list:

            if '2008' in url:
                selenium_get(url)
                yield scrapy.Request(url, callback=self.parse_2008)
            if '2009' in url:
                selenium_get(url)
                yield scrapy.Request(url, callback=self.parse_2009)

    def add_url_nums(self, urls):
        global u15_game_url_nums
        u15_game_url_nums += urls

    def add_url_exist_nums(self, url):
        global u15_game_url_exist
        u15_game_url_exist += url

    def get_url_rate(self, game_url, game_url_exist):
        return game_url_exist/game_url

# 以下2009、2008年用

    def parse_2008(self, response):
        print("response.css========" +
              str(response.css('#ContentsLeft tr td div.l_team::text').extract()))
#mainContents-innner > div.match_title2 > img
        for data in response.css('#ContentsLeft table tr'):
            team_home = data.css(
                'td div.l_team::text').extract_first()
            if team_home == None:
                continue
            item = SoccerProjItem()
            item['team_home'] = team_home
            item['team_away'] = data.css('td div.r_team::text').extract_first()
            date = data.css('td::text').extract()[1]
            item['year'] = '20' + re.search('0[0-9]', date).group()
            if '/' in date:
                item['month'] = re.search(
                    '/[0-9]+', date).group().replace("/", "")
                print("month = " + item['month'])
                item['day'] = re.sub('../../', '', date)
                print("day= " + item['day'])
            elif '.' in date:
                item['month'] = re.search(
                    '\.[0-9]+', date).group().replace(".", "")
                item['day'] = re.sub("..\...\.", '', date)
            item['leagu_name'] = response.css(
                '#mainContents-innner > div.match_title2 > img::attr(alt)').extract_first()
            item['id'] = data.css('td::text').extract()[0]
            href = data.css('td a::attr(href)').extract_first()
            item['url'] = response.urljoin(href)
            score = data.css(
                'td div.score::text').extract_first()
            item['results_home'] = re.search('[0-9]+', score).group()
            if re.search(
                    "\-[0-9]+", score):
                score_away = re.search(
                    "\-[0-9]+", score).group().replace('-', '')
                item['results_away'] = score_away
            elif re.search(
                    "\- [0-9]+", score):
                score_away2 = re.search(
                    "\- [0-9]+", score).group().replace("- ", "")
                item['results_away'] = score_away2
            yield item

    def parse_2009(self, response):
        print("response.css========" +
              str(response.css('#ContentsLeft tr td div.l_team::text').extract()))
#mainContents-innner > div.match_title2 > img
        for data in response.css('#ContentsLeft table tr'):
            team_home = data.css(
                'td div.l_team::text').extract_first()
            if team_home == None:
                continue
            item = SoccerProjItem()
            item['team_home'] = team_home
            item['team_away'] = data.css('td div.r_team::text').extract_first()
            date = data.css('td::text').extract()[1]
            item['year'] = '20' + re.search('0[0-9]', date).group()
            if '/' in date:
                item['month'] = re.search(
                    '/[0-9]+', date).group().replace("/", "")
                print("month = " + item['month'])
                item['day'] = re.sub('../../', '', date)
                print("day= " + item['day'])
            elif '.' in date:
                item['month'] = re.search(
                    '\.[0-9]+', date).group().replace(".", "")
                item['day'] = re.sub("..\...\.", '', date)
            item['leagu_name'] = "高円宮杯第21回全日本ユース（U-15）サッカー選手権大会"
            item['id'] = data.css('td::text').extract()[0]
            href = data.css('td a::attr(href)').extract_first()
            item['url'] = response.urljoin(href)
            score = data.css(
                'td div.score::text').extract_first()
            item['results_home'] = re.search('[0-9]+', score).group()
            if re.search(
                    "\-[0-9]+", score):
                score_away = re.search(
                    "\-[0-9]+", score).group().replace('-', '')
                item['results_away'] = score_away
            elif re.search(
                    "\- [0-9]+.", score):
                score_away2 = re.search(
                    "\- [0-9]+", score).group().replace("- ", "")
                item['results_away'] = score_away2
            yield item

    def closed(self, response):
        selenium_close()

#  実行時CSVに書き出す場合はーーーーー　scrapy crawl SoccerSpider -o results/soccer.csv
