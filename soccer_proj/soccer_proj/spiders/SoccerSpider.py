# -*- coding: utf-8 -*-
import scrapy
import pprint
from ..items import SoccerProjItem
from ..selenium_middleware import *
import re
# from sclapy_selenium import SeleniumRequest

# yield SeleniumRequest(url=url, callback=self.parse_result)


class SoccerspiderSpider(scrapy.Spider):
    name = 'SoccerSpider'
    allowed_domains = ['jfa.jp']
    # 高円宮杯U18サッカープレミアリーグ
    start_urls = [
        'http://www.jfa.jp/match/takamado_jfa_u18_premier2019/']
    # 高円宮杯U15サッカー選手権大会
    # start_urls = ['']
    # U12サッカー選手権大会

    custom_setting = {
        "DOWNLOAD_MIDDLEWARE": {
            "scrapy_list.selenium_middleware.ScrapyListSpiderMiddleware"
        },
        "DOWNLOAD_DELAY": 5.0,
    }

    def start_requests(self):
        # ここに取得したい試合結果一覧のURLをかく
        # url = "http://www.jfa.jp/match/takamado_jfa_u18_premier2019/east/schedule_result/"
        # url = "http://www.jfa.jp/match/takamado_jfa_u18_premier2019/west/schedule_result/"
        # url = "http://www.jfa.jp/match/takamado_jfa_u18_premier2018/east/schedule_result/"
        # url = "http://www.jfa.jp/match/takamado_jfa_u18_premier2018/west/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u18_2017/premier_2017/east/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u18_2017/premier_2017/west/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u18_2016/premier_2016/east/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u18_2016/premier_2016/west/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u18_2015/premier_2015/east/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u18_2015/premier_2015/west/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u18_2014/2014/premier/east/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u18_2014/2014/premier/west/schedule_result/"
        url = "http://www.jfa.or.jp/match/matches/2013/premier_league/east/match/index2.html"

        # 以下2014年以降用
        # # ここで、ブラウザを起動してページを開く
        # selenium_get(url)
        # # get_aで各試合の詳細URLのa要素を取得
        # alist = get_a('li.score a')
        # # for文を回してそれぞれのhref属性を取得
        # for a in alist:
        #     page = a.get_attribute('href')
        #     # それぞれのURLにおいてScrapyRequestを生成
        #     yield scrapy.Request(page, callback=self.parse)

        # 以下2013年以前用
        # ここで、ブラウザを起動してページを開く
        selenium_get(url)
        # get_aで各試合の詳細URLのa要素を取得
        next = get_a(
            '#u18wrapper > div > div.mainarea > div > div > a:nth-child(2)')
        next = next[0]
        next_url = next.get_attribute('href')

        alist = get_a('div.mainarea a')
        # u18wrapper > div > div.mainarea > div > table > tbody > tr:nth-child(2) > td:nth-child(6) > a
        # for文を回してそれぞれのhref属性を取得
        for a in alist:
            page = a.get_attribute('href')
            # それぞれのURLにおいてScrapyRequestを生成
            # yield scrapy.Request(page, callback=self.parse)
            yield scrapy.Request(page, callback=self.parse2)

        selenium_get(next_url)
        next_alist = get_a('div.mainarea a')
        for a in next_alist:
            page = a.get_attribute('href')
            # それぞれのURLにおいてScrapyRequestを生成
            # yield scrapy.Request(page, callback=self.parse)
            yield scrapy.Request(page, callback=self.parse2)

    # def start_requests(self):
    #     # ここに取得したい試合結果一覧のURLをかく
    #     domain = 'http://www.jfa.jp'
    #     # 高円宮杯U18サッカープレミアリーグ
    #     url = "http://www.jfa.jp/match/takamado_jfa_u18_premier2019/"
    #     # 高円宮杯U15サッカー選手権大会

    #     # U12サッカー選手権大会

    #     # ここで、ブラウザを起動してページを開く
    #     selenium_get(url)
    #     past_games_url = self.get_past_games_url(url, domain)
    #     east_game_results, west_game_results = self.get_game_results(
    #         past_games_url)
    #     east_game_results_url = self.get_game_results_url(east_game_results)
    #     west_game_results_url = self.get_game_results_url(west_game_results)
    #     print("east_game_results_url=====" + str(east_game_results_url))
    #     print("west_game_results_url=====" + str(west_game_results_url))

    #     for a in east_game_results_url:
    #         selenium_get(a)
    #         print("スクレイプスタートーーーーーーー")
    #         alist = get_doms('li.score a')
    #         game_detail_url_list = self.get_game_detail_url(alist)
    #         for url in game_detail_url_list:
    #             yield scrapy.Request(url, callback=self.parse)

    # def get_past_games_url(self, url, domain):
    #     count = 0
    #     past_games = get_doms('#select-year2 > option')
    #     domain = domain
    #     past_games_url = []
    #     for a in past_games:
    #         count += 1
    #         if count < 3:
    #             temp = a.get_attribute('value')
    #             if 'http' in temp:
    #                 past_game_url = temp
    #             else:
    #                 past_game_url = domain + temp
    #             past_games_url.append(past_game_url)
    #         else:
    #             break
    #     print('past_games_url==========' + str(past_games_url))
    #     return past_games_url  # 各年度のURL

    # # 以下の関数で各年度のURLから「日程・結果」を引き出す
    # def get_game_results(self, past_games_url):
    #     east_game_results = []
    #     west_game_results = []
    #     for a in past_games_url:
    #         # これで年度のページを開く
    #         selenium_get(a)
    #         # east_game_result = get_dom(
    #         #     'ul > li:nth-child(1) a')
    #         east_game_result = get_dom(
    #             '#east-category-area > ul > li:nth-child(1) a')
    #         east_game_results.append(east_game_result)
    #         # west_game_result = get_dom(
    #         #     '#west-category-area > ul > li:nth-child(1) a')
    #         west_game_result = get_dom(
    #             '#west-category-area > ul > li:nth-child(1) a')
    #         west_game_results.append(west_game_result)
    #     return east_game_results, west_game_results

    # def get_game_results_url(self, game_results):
    #     game_results_url = []
    #     for a in game_results:
    #         game_result_url = a.get_attribute('href')
    #         game_results_url.append(game_result_url)
    #     return game_results_url

    # def get_game_detail_url(self, alist):
    #     game_detail_url_list = []
    #     for a in alist:
    #         game_detail_url = a.get_attribute('href')
    #         game_detail_url_list.append(game_detail_url)
    #     return game_detail_url_list

    # def parse(self, response):
    #     print('response====================' + str(response))
    #     item = SoccerProjItem()
    #     item['leagu_name'] = response.css(
    #         '#ttl_sp > img::attr(alt)').extract_first()
    #     # いったんtempとして値を取得しているが、ここから後は正規表現だの、Splitみたいなので不要な文字列を削って出力すればよし
    #     temp = response.css(
    #         '#inner-header-score > div.text-schedule::text').extract_first()
    #     item['team_home'] = response.css(
    #         '#score-board-header > div:nth-child(1) > p:nth-child(2)::text').extract_first()
    #     item['team_away'] = response.css(
    #         '#score-board-header > div:nth-child(5) > p:nth-child(2)::text').extract_first()
    #     item['url'] = response.url
    #     results_home = response.css(
    #         '#score-board-header > div:nth-child(2)::text').extract_first()
    #     if results_home:
    #         item['results_home'] = results_home
    #     else:
    #         item['results_home'] = 'None'

    #     results_away = response.css(
    #         '#score-board-header > div:nth-child(4)::text').extract_first()
    #     if results_away:
    #         item['results_away'] = results_away
    #     else:
    #         item['results_away'] = 'None'

    #     year_pattern = '20[0-9]{2}'
    #     item['year'] = re.findall(year_pattern, temp)
    #     # item['year'] = re.search(year_pattern, temp).group()
    #     month_pattern = '[0-1][0-9]月'
    #     item['month'] = re.findall(month_pattern, temp)
    #     day_pattern = '[0-3][0-9]日'
    #     item['day'] = re.findall(day_pattern, temp)
    #     # 以下試合がまだ行われていないデータにはNoneを入れる
    #     goal_home = response.css(
    #         '#game-content-wrap > div.scorerLeft::text').extract()
    #     if goal_home:

    #         item['goal_home'] = goal_home
    #     else:
    #         item['goal_home'] = 'None'

    #     goal_away = response.css(
    #         '#game-content-wrap > div.scorerRight::text').extract()
    #     if goal_away:
    #         item['goal_away'] = goal_away
    #     else:
    #         item['goal_away'] = 'None'
    #     # time_temp = response.css('#game-content-wrap::text').extract()
    #     # print("time_temp =========" + time_temp)
    #     item['id'] = re.search('[0-9]{3,4}', temp).group()
    #     if item['id'][-1] == 0:
    #         item['round'] = re.search('第[0-9]+節', temp).group() + '10'
    #     else:
    #         item['round'] = re.search(
    #             '第[0-9]+節', temp).group() + item['id'][-1]

    #     item['time'] = []
    #     for elem in item['goal_home']:
    #         temp = re.findall('.*分', elem)
    #         if temp:
    #             item['time'].append(temp)
    #         else:
    #             continue

    #     for elem in item['goal_away']:
    #         temp = re.findall('.*分', elem)
    #         if temp:
    #             item['time'].append(temp)
    #         else:
    #             continue

    #     print('time=' + str(item['time']))

    #     yield item

    def parse2(self, response):
        print('response====================' + str(response))
        item = SoccerProjItem()
        item['leagu_name'] = response.css(
            '#u18wrapper > p > img:nth-child(1)::attr(alt)').extract_first()
        # いったんtempとして値を取得しているが、ここから後は正規表現だの、Splitみたいなので不要な文字列を削って出力すればよし
        temp = response.css(
            '#u18wrapper > div > div.mainarea > div > p.matchtitle::text').extract_first()
        item['team_home'] = response.css(
            '#u18wrapper > div > div.mainarea > div > div.matchteam.clearfix > p.matchteam1::text').extract_first()
        extract_team_home = re.findall('(.{2, 4})', item['team_home'])
        item['team_home'] = item['team_home'].strip(extract_team_home)
        item['team_away'] = response.css(
            '#u18wrapper > div > div.mainarea > div > div.matchteam.clearfix > p.matchteam2::text').extract_first()
        extract_team_away = re.findall('(.{2, 4})', item['team_away'])
        item['team_away'] = item['team_away'].strip(extract_team_away)
        item['url'] = response.url
        results_home = response.css(
            '#u18wrapper > div > div.mainarea > div > div.resultarea.clearfix > p.point1::text').extract_first()
        if results_home:
            item['results_home'] = results_home
        else:
            item['results_home'] = 'None'

        results_away = response.css(
            '#u18wrapper > div > div.mainarea > div > div.resultarea.clearfix > p.point2::text').extract_first()
        if results_away:
            item['results_away'] = results_away
        else:
            item['results_away'] = 'None'

        year_pattern = '20[0-9]{2}'
        item['year'] = re.findall(year_pattern, temp)
        # item['year'] = re.search(year_pattern, temp).group()
        month_pattern = '[0-1][0-9]月'
        item['month'] = re.findall(month_pattern, temp)
        day_pattern = '[0-3][0-9]日'
        item['day'] = re.findall(day_pattern, temp)
        # 以下試合がまだ行われていないデータにはNoneを入れる
        goal_home = response.css(
            '#u18wrapper > div > div.mainarea > div > table > tbody > tr > td.matchgoal1::text').extract()
        if goal_home:

            item['goal_home'] = goal_home
        else:
            item['goal_home'] = 'None'

        goal_away = response.css(
            '#u18wrapper > div > div.mainarea > div > table > tbody > tr > td.matchgoal2::text').extract()
        if goal_away:
            item['goal_away'] = goal_away
        else:
            item['goal_away'] = 'None'
        # time_temp = response.css('#game-content-wrap::text').extract()
        # print("time_temp =========" + time_temp)
        # item['id'] = re.search('[0-9]{3,4}', temp).group()
        temp2 = response.css(
            '#u18wrapper > div > div.mainarea > div > p.league.matcheast::text').extract()
        round_num = re.search('No..', temp2)
        round_num = round_num.strip('No.')
        item['round'] = re.search('第[0-9]+節', temp2).group() + round_num
        item['time'] = []
        for elem in item['goal_home']:
            temp = re.findall('.*分', elem)
            if temp:
                item['time'].append(temp)
            else:
                continue

        for elem in item['goal_away']:
            temp = re.findall('.*分', elem)
            if temp:
                item['time'].append(temp)
            else:
                continue

        print('time=' + str(item['time']))

        yield item

    def closed(self, response):
        selenium_close()

    # year = scrapy.Field()
    # month = scrapy.Field()
    # day = scrapy.Field()
    # goal_home = scrapy.Field()
    # goal_away = scrapy.Field()
    # time = scrapy.Field()
    # player = scrapy.Field()

    #  CSVに書き出す場合はーーーーー　scrapy crawl SoccerSpider -o results/soccer.csv

        # 違うサイトを参考にして見たミドルウェアの書き方（Chromeの場合）
        # def start_requests(self):
        #     url = "http://www.jfa.jp/match/takamado_jfa_u18_premier2019/east/schedule_result/"
        #     selenium_get(url)
        #     links = get_dom('')
        #     yield scrapy.Request()

        # def parse(self, response):
        #     for table in response.css('#main-colum > div.section-block > div.shcedule-tournament.js-createSchedule > div:nth-child(1) > div.table-wrap-tournament > table'):
        #         item = SoccerProjItem()
        #         item['headline'] = table.xpath(
        #             '//tbody/tr[1]/td[2]/text()').extract()
        #         yield item

        # -------------------------------------
        # test
        #     def parse(self, response):
        #         for sample in response.css('html body.match.premier-lower.local-east_schedule div#container.outer-block.clearfix div#main-colum div.section-block div.shcedule-tournament.js-createSchedule'):
        #             item = SoccerProjItem()
        #             item['headline'] = sample.css('#sectionNo1::text').extracted()
        #             yield item

        #     def closed(self, reasion):
        #         close_driver()
        # ---------------------------------------------

        # def parse(self, response):
        #     for topic in response.css('#main-colum > div.section-block > div.shcedule-tournament.js-createSchedule > div:nth-child(1) > div.table-wrap-tournament > table > tbody > tr:nth-child(1) > td:nth-child(3) > div.tdWrap1 > ul > li.score > a::attr(href)'):
        #         item = SoccerProjItem()
        #         item['headline'] = topic.css('a::text').extract_first()
        #         print(item['headline'])
        #         page = topic.css('a::attr(href)').extract_first()
        #         print("0000000000000000000000000000000")
        #         print(page)
        #         yield scrapy.Request(topic.css('a::attr(href)').extract_first(), callback=self.parse_detail, meta={'item': item})

        # def parse_detail(self, response):
        #     item = response.meta['item']
        #     item['url'] = response.url
        #     item['team_home'] = response.css(
        #         'div.score-board-header p::text').extract_first()
        #     yield item
