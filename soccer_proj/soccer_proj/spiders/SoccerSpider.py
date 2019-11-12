# -*- coding: utf-8 -*-
import scrapy
import pprint
from ..items import SoccerProjItem
from ..selenium_middleware import *
import re
# from sclapy_selenium import SeleniumRequest

# yield SeleniumRequest(url=url, callback=self.parse_result)

#  実行時CSVに書き出す場合はーーーーー　scrapy crawl SoccerSpider -o results/soccer.csv

u18_game_url_nums = 0
u18_game_url_exist = 0


class SoccerspiderSpider(scrapy.Spider):
    name = 'SoccerSpider'
    allowed_domains = ['jfa.jp']
    # 高円宮杯U18サッカープレミアリーグ
    start_urls = [
        'http://www.jfa.jp/match/takamado_jfa_u18_premier2019/']
    # 高円宮杯u18サッカー選手権大会
    # start_urls = ['']
    # U12サッカー選手権大会

    custom_setting = {
        "DOWNLOAD_MIDDLEWARE": {
            "scrapy_list.selenium_middleware.ScrapyListSpiderMiddleware"
        },
        "DOWNLOAD_DELAY": 5.0,
    }

    def start_requests(self):

        url_list = [
            "http://www.jfa.jp/match/takamado_jfa_u18_premier2019/east/schedule_result/",
            "http://www.jfa.jp/match/takamado_jfa_u18_premier2019/west/schedule_result/",
            "http://www.jfa.jp/match/takamado_jfa_u18_premier2018/east/schedule_result/",
            "http://www.jfa.jp/match/takamado_jfa_u18_premier2018/west/schedule_result/",
            "http://www.jfa.jp/match/prince_takamado_trophy_u18_2017/premier_2017/east/schedule_result/",
            "http://www.jfa.jp/match/prince_takamado_trophy_u18_2017/premier_2017/west/schedule_result/",
            "http://www.jfa.jp/match/prince_takamado_trophy_u18_2016/premier_2016/east/schedule_result/",
            "http://www.jfa.jp/match/prince_takamado_trophy_u18_2016/premier_2016/west/schedule_result/",
            "http://www.jfa.jp/match/prince_takamado_trophy_u18_2015/premier_2015/east/schedule_result/",
            "http://www.jfa.jp/match/prince_takamado_trophy_u18_2015/premier_2015/west/schedule_result/",
            "http://www.jfa.jp/match/prince_takamado_trophy_u18_2014/2014/premier/east/schedule_result/",
            "http://www.jfa.jp/match/prince_takamado_trophy_u18_2014/2014/premier/west/schedule_result/",
            "http://www.jfa.or.jp/match/matches/2013/premier_league/east/match/index2.html",
            "http://www.jfa.or.jp/match/matches/2013/premier_league/west/match/index2.html",
            "http://www.jfa.or.jp/match/matches/2012/premier_league/east/match/index2.html",
            "http://www.jfa.or.jp/match/matches/2012/premier_league/west/match/index2.html",
            "http://www.jfa.or.jp/match/matches/2011/premier_league/east/match/index2.html",
            "http://www.jfa.or.jp/match/matches/2011/premier_league/west/match/index2.html"
        ]
        for url in url_list:
            if any((s in url) for s in ['2019', '2018', '2017', '2016', '2015']):
                # 以下2014年以降用-------------------------------------------------------
                # ここで、ブラウザを起動してページを開く
                selenium_get(url)
                # get_aで各試合の詳細URLのa要素を取得
                alist = get_a('li.score a')
                self.add_url_nums(len(alist))

                # for文を回してそれぞれのhref属性を取得
                for a in alist:
                    page = a.get_attribute('href')
                    # それぞれのURLにおいてScrapyRequestを生成
                    yield scrapy.Request(page, callback=self.parse)
            elif '2014' in url:
                selenium_get(url)
                # get_aで各試合の詳細URLのa要素を取得
                alist = get_a('li.score a')
                self.add_url_nums(len(alist))

                # for文を回してそれぞれのhref属性を取得
                for a in alist:
                    page = a.get_attribute('href')
                    # それぞれのURLにおいてScrapyRequestを生成
                    yield scrapy.Request(page, callback=self.parse_2014)
                # ------------------------------------------------------------------------------------
            elif any((s in url) for s in ['2013', '2012']):
                # 以下2013年以前用-----------------------------------------
                # ここで、ブラウザを起動してページを開く
                selenium_get(url)
                # get_aで各試合の詳細URLのa要素を取得
                next = get_a(
                    '#u18wrapper > div > div.mainarea > div > div > a:nth-child(2)')

                next = next[0]
                next_url = next.get_attribute('href')
                # 2012、13年は以下を使用。-------------------------
                alist = get_a(
                    'div.mainarea div > table > tbody td:nth-child(6) a')
                self.add_url_nums(len(alist))
                # for文を回してそれぞれのhref属性を取得
                pages = []
                for a in alist:
                    page = a.get_attribute('href')
                    pages.append(page)

                for page in pages:
                    yield scrapy.Request(page, callback=self.parse2)

                selenium_get(next_url)
                # 2012、13年の場合は以下を使用。----------------------------------------
                next_alist = get_a(
                    'div.mainarea div > table > tbody td:nth-child(6) a')
                self.add_url_nums(len(next_alist))
                next_pages = []
                for a in next_alist:
                    next_page = a.get_attribute('href')
                    next_pages.append(next_page)

                for next_page in next_pages:
                    yield scrapy.Request(next_page, callback=self.parse2)

            elif '2011' in url:
                # ここで、ブラウザを起動してページを開く
                selenium_get(url)
                # get_aで各試合の詳細URLのa要素を取得
                next = get_a(
                    '#u18wrapper > div > div.mainarea > div > div > a:nth-child(2)')

                next = next[0]
                next_url = next.get_attribute('href')
                print("next_url ========== " + next_url)
                # 2011年はサイト構造が違うため以下を使用。--------------------------------------
                alist = get_a(
                    'div.mainarea div > table > tbody td:nth-child(5) a')
                self.add_url_nums(len(alist))
                # for文を回してそれぞれのhref属性を取得
                pages = []
                for a in alist:
                    page = a.get_attribute('href')
                    pages.append(page)
                for page in pages:
                    yield scrapy.Request(page, callback=self.parse2)

                selenium_get(next_url)
                # 2011年のモノはサイト構造が違うため、以下を使用。--------------------------------
                next_alist = get_a(
                    'div.mainarea div > table > tbody td:nth-child(5) a')
                self.add_url_nums(len(next_alist))
                print("url nums ============ " + str(u18_game_url_nums))
                next_pages = []
                for a in next_alist:
                    next_page = a.get_attribute('href')
                    next_pages.append(next_page)

                for next_page in next_pages:
                    yield scrapy.Request(next_page, callback=self.parse2)

    def add_url_nums(self, urls):
        global u18_game_url_nums
        u18_game_url_nums += urls

    def add_url_exist_nums(self, url):
        global u18_game_url_exist
        u18_game_url_exist += url

    def get_u18_url_nums(self):
        global u18_game_url_nums
        return u18_game_url_nums

    def get_u18_url_exist_nums(self):
        global u18_game_url_exist
        return u18_game_url_exist

    def get_url_rate(self, game_url, game_url_exist):
        return game_url_exist/game_url

        # # 以下はU18の年度によってサイト構成が違うものを自動化する段階（途中）－－－－－－－－－－－－－－－－－－－－－－－－
        # selenium_get(url)
        # url = "http://www.jfa.jp/match/takamado_jfa_u18_premier2019/"
        # domain = "http://www.jfa.jp"
        # past_games_urls = self.get_past_games_url(url, domain)
        # print("past_game-Url == == == ===" + str(past_games_urls))

        # # get_aで各試合の詳細URLのa要素を取得
        # next = get_a(
        #     '#u18wrapper > div > div.mainarea > div > div > a:nth-child(2)')

        # next = next[0]
        # next_url = next.get_attribute('href')
        # print("next_url ========== " + next_url)
        # # 2012、13年は以下を使用。
        # # alist = get_a('div.mainarea div > table > tbody td:nth-child(6) a')
        # # 2011年はサイト構造が違うため以下を使用。
        # alist = get_a('div.mainarea div > table > tbody td:nth-child(5) a')
        # # for文を回してそれぞれのhref属性を取得
        # pages = []
        # for a in alist:
        #     page = a.get_attribute('href')
        #     pages.append(page)
        #     print("page ============ " + page)

        # for page in pages:
        #     yield scrapy.Request(page, callback=self.parse2)

        # selenium_get(next_url)
        # # 2012、13年の場合は以下を使用。
        # # next_alist = get_a(
        # #     'div.mainarea div > table > tbody td:nth-child(6) a')
        # # 2011年のモノはサイト構造が違うため、以下を使用。
        # next_alist = get_a(
        #     'div.mainarea div > table > tbody td:nth-child(5) a')
        # next_pages = []
        # for a in next_alist:
        #     next_page = a.get_attribute('href')
        #     next_pages.append(next_page)

        # for next_page in next_pages:
        #     yield scrapy.Request(next_page, callback=self.parse2)

    # def start_requests(self):
    #     # ここに取得したい試合結果一覧のURLをかく
    #     domain = 'http://www.jfa.jp'
    #     # 高円宮杯U18サッカープレミアリーグ
    #     url = "http://www.jfa.jp/match/takamado_jfa_u18_premier2019/"
    #     # 高円宮杯u18サッカー選手権大会

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
    #     past_games = get_doms('#select-year2 > option')
    #     domain = domain
    #     past_games_url = []
    #     for a in past_games:
    #         temp = a.get_attribute('value')
    #         if 'http' in temp:
    #             past_game_url = temp
    #         else:
    #             past_game_url = domain + temp
    #         past_games_url.append(past_game_url)
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
        # ここまでーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

    def parse(self, response):
        item = SoccerProjItem()
        item['leagu_name'] = response.css(
            '#ttl_sp > img::attr(alt)').extract_first()
        # いったんtempとして値を取得しているが、ここから後は正規表現だの、Splitみたいなので不要な文字列を削って出力すればよし
        temp = response.css(
            '#inner-header-score > div.text-schedule::text').extract_first()
        item['team_home'] = response.css(
            '#score-board-header > div:nth-child(1) > p:nth-child(2)::text').extract_first()
        # item['team_home'] = response.css(
        #     '#score-board-header > div:nth-child(1)::text').extract_first()

        # item['team_away'] = response.css(
        #     '#score-board-header > div:nth-child(5)::text').extract_first()
        item['team_away'] = response.css(
            '#score-board-header > div:nth-child(5) > p:nth-child(2)::text').extract_first()
        item['url'] = response.url
        if item['url']:
            self.add_url_exist_nums(1)
            global u18_game_url_exist
            global u18_game_url_nums
            rate = self.get_url_rate(u18_game_url_nums, u18_game_url_exist)
            print("rate===========" + str(rate))
        print("nums url exist===========" + str(u18_game_url_exist))
        results_home = response.css(
            '#score-board-header > div:nth-child(2)::text').extract_first()
        if results_home:
            item['results_home'] = results_home
        else:
            item['results_home'] = 'None'

        results_away = response.css(
            '#score-board-header > div:nth-child(4)::text').extract_first()
        if results_away:
            item['results_away'] = results_away
        else:
            item['results_away'] = 'None'

        year_pattern = '20[0-9]{2}'
        if re.search(year_pattern, temp):
            item['year'] = re.search(year_pattern, temp).group(0)
        else:
            item['year'] = '未定'
        # item['year'] = re.search(year_pattern, temp).group()
        month_pattern = '[0-1][0-9]月'
        item['month'] = re.findall(month_pattern, temp)
        day_pattern = '[0-3][0-9]日'
        item['day'] = re.findall(day_pattern, temp)
        # 以下試合がまだ行われていないデータにはNoneを入れる
        goal_home = response.css(
            '#game-content-wrap > div.scorerLeft::text').extract()
        if goal_home:

            item['goal_home'] = goal_home
        else:
            item['goal_home'] = 'None'

        goal_away = response.css(
            '#game-content-wrap > div.scorerRight::text').extract()
        if goal_away:
            item['goal_away'] = goal_away
        else:
            item['goal_away'] = 'None'
        item['id'] = re.search('[0-9]{3,4}', temp).group()
        if item['id'][-1] == 0:
            item['round'] = re.search('第[0-9]+節', temp).group() + '10'
        else:
            item['round'] = re.search(
                '第[0-9]+節', temp).group() + item['id'][-1]

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

        yield item

    def parse_2014(self, response):
        item = SoccerProjItem()
        item['leagu_name'] = response.css(
            '#ttl_sp > img::attr(alt)').extract_first()
        # いったんtempとして値を取得しているが、ここから後は正規表現だの、Splitみたいなので不要な文字列を削って出力すればよし
        temp = response.css(
            '#inner-header-score > div.text-schedule::text').extract_first()
        # item['team_home'] = response.css(
        #     '#score-board-header > div:nth-child(1) > p:nth-child(2)::text').extract_first()
        item['team_home'] = response.css(
            '#score-board-header > div:nth-child(1)::text').extract_first()

        item['team_away'] = response.css(
            '#score-board-header > div:nth-child(5)::text').extract_first()
        # item['team_away'] = response.css(
        #     '#score-board-header > div:nth-child(5) > p:nth-child(2)::text').extract_first()
        item['url'] = response.url
        if item['url']:
            self.add_url_exist_nums(1)
            global u18_game_url_exist
            global u18_game_url_nums
            rate = self.get_url_rate(u18_game_url_nums, u18_game_url_exist)
            print("rate===========" + str(rate))
        print("nums url exist===========" + str(u18_game_url_exist))
        results_home = response.css(
            '#score-board-header > div:nth-child(2)::text').extract_first()
        if results_home:
            item['results_home'] = results_home
        else:
            item['results_home'] = 'None'

        results_away = response.css(
            '#score-board-header > div:nth-child(4)::text').extract_first()
        if results_away:
            item['results_away'] = results_away
        else:
            item['results_away'] = 'None'

        year_pattern = '20[0-9]{2}'
        item['year'] = re.search(year_pattern, temp).group(0)
        # item['year'] = re.search(year_pattern, temp).group()
        month_pattern = '[0-1][0-9]月'
        item['month'] = re.findall(month_pattern, temp)
        day_pattern = '[0-3][0-9]日'
        item['day'] = re.findall(day_pattern, temp)
        # 以下試合がまだ行われていないデータにはNoneを入れる
        goal_home = response.css(
            '#game-content-wrap > div.scorerLeft::text').extract()
        if goal_home:

            item['goal_home'] = goal_home
        else:
            item['goal_home'] = 'None'

        goal_away = response.css(
            '#game-content-wrap > div.scorerRight::text').extract()
        if goal_away:
            item['goal_away'] = goal_away
        else:
            item['goal_away'] = 'None'
        item['id'] = re.search('[0-9]{3,4}', temp).group()
        if item['id'][-1] == 0:
            item['round'] = re.search('第[0-9]+節', temp).group() + '10'
        else:
            item['round'] = re.search(
                '第[0-9]+節', temp).group() + item['id'][-1]

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

        yield item

    def parse2(self, response):
        item = SoccerProjItem()
        item['leagu_name'] = response.css(
            '#u18wrapper > p > img:nth-child(1)::attr(alt)').extract_first()
        # いったんtempとして値を取得しているが、ここから後は正規表現だの、Splitみたいなので不要な文字列を削って出力すればよし
        temp = response.css(
            '#u18wrapper > div > div.mainarea > div > p.matchtitle::text').extract_first()
        item['team_home'] = response.css(
            '#u18wrapper > div > div.mainarea > div > div.matchteam.clearfix > p.matchteam1::text').extract_first()
        extract_team_home = re.findall("（.+）", item['team_home'])
        item['team_home'] = item['team_home'].replace(extract_team_home[0], "")
        item['team_home'] = item['team_home'].strip()
        item['team_away'] = response.css(
            '#u18wrapper > div > div.mainarea > div > div.matchteam.clearfix > p.matchteam2::text').extract_first()
        extract_team_away = re.findall('（.+）', item['team_away'])
        item['team_away'] = item['team_away'].replace(extract_team_away[0], "")
        item['team_away'] = item['team_away'].strip()
        item['url'] = response.url
        if item['url']:
            self.add_url_exist_nums(1)
            global u18_game_url_exist
            global u18_game_url_nums
            rate = self.get_url_rate(u18_game_url_nums, u18_game_url_exist)
            print("rate===========" + str(rate))
        print("nums url exist===========" + str(u18_game_url_exist))
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
        item['year'] = re.search(year_pattern, temp).group()
        # item['year'] = re.search(year_pattern, temp).group()
        month_pattern = '[0-1][0-9]月'
        item['month'] = re.findall(month_pattern, temp)
        day_pattern = '[0-3][0-9]日'
        item['day'] = re.findall(day_pattern, temp)
        # 以下試合がまだ行われていないデータにはNoneを入れる
        # ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        #u18wrapper > div > div.mainarea > div > table > tbody > tr > td.matchgoal1
        goal_home = response.css(
            'td.matchgoal1::text').extract()
        # print("goal_home ===== " + str(goal_home))
        if goal_home:
            # item['goal_home'] = " ".join(goal_home).strip().replace('分 ', '分,')
            # item['goal_home'] = " ".join(goal_home).strip().replace('\n', ',')
            goal_home = list(map(lambda x: x.strip(), goal_home))
            # print("goal_home2 ===== " + str(goal_home))
            item['goal_home'] = goal_home
        else:
            item['goal_home'] = 'None'

        goal_away = response.css(
            'td.matchgoal2::text').extract()
        if goal_away:
            # item['goal_away'] = " ".join(
            #     goal_away).strip().replace(' [0-9]+分 ', ',[0-9]+分')
            goal_away = list(map(lambda x: x.strip(), goal_away))
            item['goal_away'] = goal_away
        else:
            item['goal_away'] = 'None'
        # time_temp = response.css('#game-content-wrap::text').extract()
        # print("time_temp =========" + time_temp)
        temp2 = response.css(
            '#u18wrapper > div > div.mainarea > div > p.league::text').extract()
        # round_num = re.search('No\..*', temp2[0]).group()
        round_num = re.search('[0-9]+', temp2[0]).group()
        # item['id'] = re.search('[0-9]{1,3}', temp2).group()
        item['id'] = re.search('[0-9]{1,3}', temp2[0]).group()

        # round_num = round_num.strip('No.')
        # print("round num ========" + round_num)
        item['round'] = re.search('第[0-9]+節', temp2[0]).group() + round_num
        item['time'] = []
        # print("temp ============ " + str(temp))
        for elem in goal_home:
            # print("elem ========= " + str(elem))
            temp = re.findall('.*分', elem)
            temp = " ".join(temp).strip()
            if temp:
                # print("temp in for stntense ====== " + str(temp))
                item['time'].append(temp)
            else:
                continue

        for elem in goal_away:
            temp = re.findall('.*分', elem)
            temp = " ".join(temp).strip()
            if temp:
                item['time'].append(temp)
            else:
                continue

        print("url nums O=========" + str(u18_game_url_nums))
        yield item

    def closed(self, response):
        selenium_close()
