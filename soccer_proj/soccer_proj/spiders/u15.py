# -*- coding: utf-8 -*-
import scrapy
import pprint
from ..items import SoccerProjItem
from ..selenium_middleware import *
import re


class U15Spider(scrapy.Spider):
    name = 'u15'
    allowed_domains = ['http://www.jfa.jp/match/takamado_jfa_u15_2019/']
    start_urls = ['http://http://www.jfa.jp/match/takamado_jfa_u15_2019//']

    custom_setting = {
        "DOWNLOAD_MIDDLEWARE": {
            "scrapy_list.selenium_middleware.ScrapyListSpiderMiddleware"
        },
        "DOWNLOAD_DELAY": 5.0,
    }

    def start_requests(self):
        # url = "http://www.jfa.jp/match/takamado_jfa_u15_2018/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u15_2017/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u15_2016/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u15_2015/schedule_result/"
        # url = "http://www.jfa.jp/match/prince_takamado_trophy_u15_2014/schedule_result/"
        # ーーーーーーーーーーーーーーーーーーーここまでCSV出力済みーーーーーーーーーーーーーーーーーーー
        # url = "http://www.jfa.or.jp/match/matches/2013/1228takamado_u15/index.html"
        # url = "http://www.jfa.or.jp/match/matches/2012/1229takamado_u15/index.html"
        # url = "http://www.jfa.or.jp/match/matches/2011/1229takamado_u15/index.html"
        url = "http://www.jfa.or.jp/match/matches/2010/takamado_u15/index.html"
        # ----------------------------------2009年以前はそもそも各試合の詳細ページが存在しない。－－－－－－－－－－

        selenium_get(url)
        # get_aで各試合の詳細URLのa要素を取得
        # 以下2014-2018年用ーーーーーーーーーーーーーーーーーーー
        # alist = get_a('li.score a')
        # 以下2013-用ーーーーーーーーーー
        alist = get_a('#Map222 > area')
        # for文を回してそれぞれのhref属性を取得
        for a in alist:
            page = a.get_attribute('href')
            print("page===============" + page)
            # それぞれのURLにおいてScrapyRequestを生成
            # yield scrapy.Request(page, callback=self.parse)
            yield scrapy.Request(page, callback=self.parse2)

    def parse(self, response):
        print('response====================' + str(response))
        item = SoccerProjItem()
        item['leagu_name'] = response.css(
            '#ttl_sp > img::attr(alt)').extract_first()
        # いったんtempとして値を取得しているが、ここから後は正規表現だの、Splitみたいなので不要な文字列を削って出力すればよし
        temp = response.css(
            '#inner-header-score > div.text-schedule::text').extract_first()
        item['team_home'] = response.css(
            '#score-board-header > div:nth-child(1) > p:nth-child(2)::text').extract_first()
        item['team_away'] = response.css(
            '#score-board-header > div:nth-child(5) > p:nth-child(2)::text').extract_first()
        item['url'] = response.url
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
        item['year'] = re.findall(year_pattern, temp)
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
        # time_temp = response.css('#game-content-wrap::text').extract()
        # print("time_temp =========" + time_temp)
        item['id'] = re.search('[0-9]{1,4}', temp).group()
        if re.search('.回戦', temp):
            item['round'] = re.search('.回戦', temp).group()
        else:
            item['round'] = re.search(
                '.+勝', temp).group()

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

    def parse2(self, response):
        print('response====================' + str(response))
        item = SoccerProjItem()
        item['leagu_name'] = response.css(
            '#mainContents-innner > div.premier_title > a > img::attr(alt)').extract_first()
        # いったんtempとして値を取得しているが、ここから後は正規表現だの、Splitみたいなので不要な文字列を削って出力すればよし
        temp = response.css(
            '#ContentsLeft > div.topTitleTxtMatchPage2.bottom10::text').extract_first()
        # print("temp===========" + str(temp))
        item['team_home'] = response.css(
            '#resultbox-inner > div.l_team::text').extract_first()
        # print("teamhome -=============" + str(item['team_home']))
        # extract_team_home = re.findall("（.+）", item['team_home'])
        # item['team_home'] = item['team_home'].replace(extract_team_home[0], "")
        item['team_home'] = item['team_home'].strip()
        item['team_away'] = response.css(
            '#resultbox-inner > div.r_team::text').extract_first()
        # extract_team_away = re.findall('（.+）', item['team_away'])
        # print("extract_team_away=========" + str(extract_team_away))
        # item['team_away'] = item['team_away'].replace(extract_team_away[0], "")
        item['team_away'] = item['team_away'].strip()
        # print("item_away ====================== " + item['team_away'])
        item['url'] = response.url
        results_home = response.css(
            '#resultbox-inner > div.score > span::text').extract()[0]
        # print("result_home ======== " + str(results_home.replace("\xa0", "")))
        if results_home:
            item['results_home'] = results_home.replace("\xa0", "")
        else:
            item['results_home'] = 'None'

        results_away = response.css(
            '#resultbox-inner > div.score > span::text').extract()[1]
        if results_away:
            item['results_away'] = results_away.replace("\xa0", "")
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
        # ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        # ここのGoalHomeの値が一向にとれない。
        # goal_home = response.xpath(
        #     '//*[@id="resultbox"]/table/tbody/tr/td[1]/text()').extract()
        goal_home = response.css(
            'td.t_right::text').extract()
        #resultbox > table > tbody > tr > td.t_right
        # print("goal home ======- " + str(goal_home))
        if goal_home:
            # item['goal_home'] = " ".join(goal_home).strip().replace(
            #     '\n', "").replace("\t", "")
            item['goal_home'] = " ".join(goal_home).replace(' ', '').replace(
                "\n", "").replace("\t", "")
        else:
            item['goal_home'] = 'None'

        goal_away = response.css('td.t_left span::text').extract()
        #resultbox > table > tbody > tr > td.t_left > span
        # print("goal_away ============ " + str(goal_away))
        if goal_away:
            item['goal_away'] = " ".join(goal_away).replace(' ', '').replace(
                "\n", "").replace("\t", "")
        else:
            item['goal_away'] = 'None'
        # time_temp = response.css('#game-content-wrap::text').extract()
        # print("time_temp =========" + time_temp)
        temp2 = response.css(
            '#ContentsLeft > div.topTitleTxt.bottom10::text').extract()
        print("temp2 ====== " + str(temp2))
        item['id'] = re.search('[0-9]+', temp2[0]).group()
        # round_num = re.search('No\..*', temp2[0]).group()
        # round_num = re.search('[0-9]', temp2[0]).group()
        # print("round num ========" + round_num)

        # round_num = round_num.strip('No.')
        # print("round num ========" + round_num)
        # item['round'] = re.search('第[0-9]+節', temp2[0]).group() + round_num
        item['time'] = []
        # print("temp ============ " + str(temp))
        if re.search('.回戦', temp2[0]):
            item['round'] = re.search('.回戦', temp2[0]).group()
        else:
            item['round'] = re.search(
                '.+勝', temp2[0]).group()
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

        # print('time=' + str(item['time']))

        yield item

    def closed(self, response):
        selenium_close()


# from sclapy_selenium import SeleniumRequest

# yield SeleniumRequest(url=url, callback=self.parse_result)

#  実行時CSVに書き出す場合はーーーーー　scrapy crawl SoccerSpider -o results/soccer.csv
