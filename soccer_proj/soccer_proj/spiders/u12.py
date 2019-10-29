# -*- coding: utf-8 -*-
import scrapy
import pprint
from ..items import SoccerProjItem
from ..selenium_middleware import *
import re


class U12Spider(scrapy.Spider):
    name = 'u12'
    allowed_domains = [
        'http://www.jfa.jp/match/japan_u12_football_championship_2019/']
    start_urls = [
        'http://http://www.jfa.jp/match/japan_u12_football_championship_2019//']
    custom_setting = {
        "DOWNLOAD_MIDDLEWARE": {
            "scrapy_list.selenium_middleware.ScrapyListSpiderMiddleware"
        },
        "DOWNLOAD_DELAY": 5.0,
    }

    def start_requests(self):

        url_list = [
            "http://www.jfa.jp/match/japan_u12_football_championship_2018/schedule_result/",
            "http://www.jfa.jp/match/japan_u12_football_championship_2017/schedule_result/",
            "http://www.jfa.jp/match/japan_u12_football_championship_2016/schedule_result/",
            "http://www.jfa.jp/match/japan_u12_football_championship_2015/schedule_result/",
            "http://www.jfa.jp/match/japan_u12_football_championship_2014/schedule_result/index.html#pankz",
            "http://www.jfa.or.jp/match/matches/2013/0803zensho/schedule_result/schedule.html",
            "http://www.jfa.or.jp/match/matches/2012/0804zensho/schedule_result/schedule.html",
            "http://www.jfa.or.jp/match/matches/2011/0806zensho/schedule_result/schedule.html"
        ]

        for url in url_list:
            if any((s in url) for s in ['2018', '2017', '2016', '2015', '2014']):
                # 以下2014-2018年用ーーーーーーーーーーーーーーーーーーー
                selenium_get(url)
                # get_aで各試合の詳細URLのa要素を取得
                alist = get_a('li.score a')
                # for文を回してそれぞれのhref属性を取得
                for a in alist:
                    page = a.get_attribute('href')
                    # それぞれのURLにおいてScrapyRequestを生成
                    yield scrapy.Request(page, callback=self.parse)

            elif any((s in url) for s in ['2013', '2012', '2011']):
                # 以下2013年ーーーーーーーーーー
                selenium_get(url)

                alist = get_a(
                    '#ContentsLeft > table > tbody > tr > td > div > a')
                count = 0
                for a in alist:
                    page = a.get_attribute('href')
                    count += 1
                    yield scrapy.Request(page, callback=self.before_parse)

    def before_parse(self, response):
        temp = response.css(
            '#mainContents table a::attr(href)').extract()
        temp_final = response.css(
            '#ContentsLeft table a::attr(href)').extract()
        temp = list(set(temp))
        temp = [elem for elem in temp if 'pdf' not in elem]
        temp = list(map(lambda x: response.url.rstrip(
            "schedule_result/schedule.html") + x.strip(".."), temp))

        if temp_final:
            temp_final = list(set(temp_final))
            temp_final = [elem for elem in temp_final if 'pdf' not in elem]
            temp_final = list(map(lambda x: response.url.replace(
                "/schedule_result/schedule.html", "") + x.strip(".."), temp_final))

        count2 = 0
        if temp:
            for detail in temp:
                item = SoccerProjItem()
                count2 += 1
                print("count2 ============================" + str(count2))
                yield scrapy.Request(detail, callback=self.parse2, meta={'item': item}, dont_filter=True)

        elif temp_final:
            for page in temp_final:
                item = SoccerProjItem()
                count2 += 1
                print("count2 ============================ " + str(count2))
                yield scrapy.Request(page, callback=self.parse2, meta={'item': item}, dont_filter=True)

    def parse(self, response):
        item = SoccerProjItem()
        item['leagu_name'] = response.css(
            '#ttl_sp > img::attr(alt)').extract_first()
        # いったんtempとして値を取得しているが、ここから後は正規表現だの、Splitみたいなので不要な文字列を削って出力すればよし
        temp = response.css(
            '#inner-header-score > div.text-schedule::text').extract_first()
        item['team_home'] = response.css(
            '#score-board-header > div:nth-child(1)::text').extract_first()
        item['team_away'] = response.css(
            '#score-board-header > div:nth-child(5)::text').extract_first()
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

        item['id'] = re.search('[0-9]{1,4}', temp).group()

        if re.search('.回戦', temp):
            item['round'] = re.search('.回戦', temp).group()
        elif re.search('第.節', temp):
            item['round'] = re.search('第.節', temp).group()
        elif re.search('ラウンド..', temp):
            item['round'] = re.search('ラウンド..', temp).group()
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
        yield item

    def parse2(self, response):
        print('response====================' + str(response))
        # item = SoccerProjItem()
        item = response.meta['item']
        leagu_name = response.css(
            'head > title::text').extract_first()
        item['leagu_name'] = re.search('第.+ー大会', leagu_name).group()
        # いったんtempとして値を取得しているが、ここから後は正規表現だの、Splitみたいなので不要な文字列を削って出力すればよし
        temp = response.css(
            '#ContentsLeft > div.topTitleTxtMatchPage2.bottom10::text').extract_first()
        item['team_home'] = response.css(
            '#resultbox-inner > div.l_team::text').extract_first()
        item['team_home'] = item['team_home'].strip()
        item['team_away'] = response.css(
            '#resultbox-inner > div.r_team::text').extract_first()
        item['team_away'] = item['team_away'].strip()
        item['url'] = response.url
        results_home = response.css(
            '#resultbox-inner > div.score > span::text').extract()[0]
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
        month_pattern = '[0-1][0-9]月'
        item['month'] = re.findall(month_pattern, temp)
        day_pattern = '[0-3][0-9]日'
        item['day'] = re.findall(day_pattern, temp)
        # 以下試合がまだ行われていないデータにはNoneを入れる
        # ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        # ここのGoalHomeの値が一向にとれない。

        goal_home = response.css(
            'td.t_right::text').extract()
        if goal_home:
            item['goal_home'] = " ".join(goal_home).replace(' ', '').replace(
                "\n", "").replace("\t", "")
        else:
            item['goal_home'] = 'None'

        goal_away = response.css(
            'td.t_left span::text').extract()
        if goal_away:
            item['goal_away'] = " ".join(goal_away).replace(' ', '').replace(
                "\n", "").replace("\t", "")
        else:
            item['goal_away'] = 'None'
        temp2 = response.css(
            '#ContentsLeft > div.topTitleTxt.bottom10::text').extract()
        item['id'] = re.search('[0-9]+', temp2[0]).group()
        if re.search('No\..*', temp2[0]):
            round_num = re.search('No\..*', temp2[0]).group()
        item['time'] = []
        if re.search('.回戦', temp2[0]):
            item['round'] = re.search('.回戦', temp2[0]).group()
        elif re.search('第[0-9]+節', temp2[0]):
            item['round'] = re.search('第[0-9]+節', temp2[0]).group() + round_num
        else:
            item['round'] = re.search(
                '.+勝', temp2[0]).group()
        for elem in goal_home:
            temp = re.findall('.*分', elem)
            temp = " ".join(temp).strip()
            if temp:
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
        yield item

    def closed(self, response):
        selenium_close()

#  実行時CSVに書き出す場合はーーーーー　scrapy crawl SoccerSpider -o results/soccer.csv
