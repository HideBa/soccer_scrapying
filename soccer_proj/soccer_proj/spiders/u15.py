# -*- coding: utf-8 -*-
import scrapy
import pprint
from ..items import SoccerProjItem
from ..selenium_middleware import *
import re

u15_game_url_nums = 0
u15_game_url_exist = 0


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
        url_list = [
            # "http://www.jfa.jp/match/takamado_jfa_u15_2018/schedule_result/",
            # "http://www.jfa.jp/match/prince_takamado_trophy_u15_2017/schedule_result/",
            # "http://www.jfa.jp/match/prince_takamado_trophy_u15_2016/schedule_result/",
            # "http://www.jfa.jp/match/prince_takamado_trophy_u15_2015/schedule_result/",
            # "http://www.jfa.jp/match/prince_takamado_trophy_u15_2014/schedule_result/",
            # "http://www.jfa.or.jp/match/matches/2013/1228takamado_u15/index.html",
            # "http://www.jfa.or.jp/match/matches/2012/1229takamado_u15/index.html",
            # "http://www.jfa.or.jp/match/matches/2011/1229takamado_u15/index.html",
            # "http://www.jfa.or.jp/match/matches/2010/takamado_u15/index.html",
            # "http://www.jfa.or.jp/match/matches/2009/takamado_u15/schedule_result/schedule.html",
            # "http://www.jfa.or.jp/match/matches/2008/takamado_u15/schedule_result/schedule.html",
            # "http://www.jfa.or.jp/archive/domestic/category_3/games/2007/takamado_jy_2007/",
            "http://www.jfa.or.jp/archive/domestic/category_3/games/2006/takamado_jy_2006/"
        ]
        # ----------------------------------2009年以前はそもそも各試合の詳細ページが存在しない。－－－－－－－－－－

        for url in url_list:
            if any((s in url) for s in ['2018', '2017', '2016', '2015', '2014']):
                selenium_get(url)
                # get_aで各試合の詳細URLのa要素を取得
                # 以下2014-2018年用ーーーーーーーーーーーーーーーーーーー
                alist = get_a('li.score a')
                self.add_url_nums(len(alist))
                # for文を回してそれぞれのhref属性を取得
                for a in alist:
                    page = a.get_attribute('href')
                    # それぞれのURLにおいてScrapyRequestを生成
                    yield scrapy.Request(page, callback=self.parse)

            elif any((s in url) for s in ['2013', '2012', '2011', '2010']):
                selenium_get(url)
                # get_aで各試合の詳細URLのa要素を取得
                # 以下2013-用ーーーーーーーーーー
                alist = get_a('#Map222 > area')
                self.add_url_nums(len(alist))
                # for文を回してそれぞれのhref属性を取得
                for a in alist:
                    page = a.get_attribute('href')
                    # それぞれのURLにおいてScrapyRequestを生成
                    yield scrapy.Request(page, callback=self.parse_2013)

            elif any((s in url) for s in ['2009', '2008']):
                selenium_get(url)
                yield scrapy.Request(url, callback=self.parse_2009)

            elif any((s in url) for s in ['2007']):
                print("start ==============")
                selenium_get(url)
                yield scrapy.Request(url, callback=self.parse_2007)

            elif any((s in url) for s in ['2006']):
                print("start ==============")
                selenium_get(url)
                yield scrapy.Request(url, callback=self.parse_2006)

    def add_url_nums(self, urls):
        global u15_game_url_nums
        u15_game_url_nums += urls

    def add_url_exist_nums(self, url):
        global u15_game_url_exist
        u15_game_url_exist += url

    def get_url_rate(self, game_url, game_url_exist):
        return game_url_exist/game_url

    def parse(self, response):
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
        if item['url']:
            self.add_url_exist_nums(1)
            global u15_game_url_exist
            global u15_game_url_nums
            rate = self.get_url_rate(u15_game_url_nums, u15_game_url_exist)
            print("rate===========" + str(rate))
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
        yield item

    def parse_2013(self, response):
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
        if item['url']:
            self.add_url_exist_nums(1)
            global u15_game_url_exist
            global u15_game_url_nums
            rate = self.get_url_rate(u15_game_url_nums, u15_game_url_exist)
            print("rate===========" + str(rate))
        print("nums url exist===========" + str(u15_game_url_exist))
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
        goal_home = response.css(
            'td.t_right::text').extract()
        if goal_home:
            goal_home = list(map(lambda x: x.strip(), goal_home))
            item['goal_home'] = goal_home
            # item['goal_home'] = " ".join(goal_home).replace(' ', '').replace(
            #     "\n", "").replace("\t", "")
        else:
            item['goal_home'] = 'None'

        goal_away = response.css('td.t_left span::text').extract()
        if goal_away:
            goal_away = list(map(lambda x: x.strip(), goal_away))
            item['goal_away'] = goal_away
            # item['goal_away'] = " ".join(goal_away).replace(' ', '').replace(
            # "\n", "").replace("\t", "")
        else:
            item['goal_away'] = 'None'
        temp2 = response.css(
            '#ContentsLeft > div.topTitleTxt.bottom10::text').extract()
        print("temp2 ====== " + str(temp2))
        item['id'] = re.search('[0-9]+', temp2[0]).group()

        item['time'] = []
        if re.search('.回戦', temp2[0]):
            item['round'] = re.search('.回戦', temp2[0]).group()
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
        print("url nums O=========" + str(u15_game_url_nums))
        yield item

# 以下2009、2008年用

    def parse_2009(self, response):
        print("response.css========" +
              str(response.css('#ContentsLeft tr td div.l_team::text').extract()))
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

    def parse_2007(self, response):
        print("----------------------------------")
        datas3 = response.css(
            'div.repCntAreaBack > div > div table:nth-child(23) tr')
        print("data3 ======= " + str(datas3.css('::text').extract()))
        for data in datas3:
            # result = data.css('td:nth-child(6) a::text').extract()
            url = data.css("td:nth-child(6) a::attr(href)").extract_first()
            # url = data.css("td:nth-child(6) a::text").extract_first()
            # url = data.css("td:nth-child(6) a::attr(href)").extract_first()
            if not url:
                continue
            url = response.urljoin(url)
            print("url ========== " + str(url))
            item = SoccerProjItem()
            yield scrapy.Request(url, callback=self.parse_2007_2, meta={'item': item}, dont_filter=True)

        datas4 = response.css(
            'div.repCntAreaBack > div > div table:nth-child(28) tr')
        for data in datas4:
            # result = data.css('td:nth-child(6) a::text').extract()
            url = data.css("td:nth-child(6) a::attr(href)").extract_first()
            # url = data.css("td:nth-child(6) a::text").extract_first()
            # url = data.css("td:nth-child(6) a::attr(href)").extract_first()
            if not url:
                continue
            url = response.urljoin(url)
            print("url ========== " + str(url))
            item = SoccerProjItem()
            yield scrapy.Request(url, callback=self.parse_2007_2, meta={'item': item}, dont_filter=True)

    def parse_2007_2(self, response):
        print("good")
        # item = SoccerProjItem()
        item = response.meta['item']
        temp = response.css(
            'div.repCntAreaBack div td span::text').extract_first()
        print("temp ========= " + temp)
        item['year'] = "20" + re.search("[0-9]+", temp).group()
        month = re.search("..\.[0-9]+", temp).group()
        # print("month = " + month)
        item['month'] = re.sub('..\.', '', month)
        day = re.search("..\...\.[0-9]+", temp).group()
        item['day'] = re.sub('..\...\.', '', day)
        item['leagu_name'] = response.css(
            'div.repCntAreaBack div p:nth-child(2) > img::attr(alt)').extract_first()
        item['team_home'] = response.css('#scoreL::text').extract_first()
        item['team_away'] = response.css('#scoreR::text').extract_first()
        item['results_home'] = response.css(
            '#scoreBoxWrap td:nth-child(2)::text').extract_first().strip()
        item['results_away'] = response.css(
            '#scoreBoxWrap td:nth-child(4)::text').extract_first().strip()
        item['goal_home'] = response.css(
            '#scorerName div:nth-child(1) span::text').extract()
        item['goal_away'] = response.css(
            '#scorerName > div:nth-child(2) > span::text').extract()
        item['time'] = []
        item['url'] = response.url
        for elem in item['goal_home']:
            temp = re.findall('.*分', elem)
            temp = " ".join(temp).strip()
            if temp:
                item['time'].append(temp)
            else:
                continue

        for elem in item['goal_away']:
            temp = re.findall('.*分', elem)
            temp = " ".join(temp).strip()
            if temp:
                item['time'].append(temp)
            else:
                continue
        # item['id'] =
        yield item

    def parse_2006(self, response):
        print("----------------------------------")
        datas3 = response.css(
            'div.repCntAreaBack > div > div table:nth-child(6) tr')
        print("data3 ======= " + str(datas3.css('::text').extract()))
        for data in datas3:
            # result = data.css('td:nth-child(6) a::text').extract()
            url = data.css("td:nth-child(3) a::attr(href)").extract_first()
            # url = data.css("td:nth-child(6) a::text").extract_first()
            # url = data.css("td:nth-child(6) a::attr(href)").extract_first()
            if not url:
                continue
            url = response.urljoin(url)
            print("url ========== " + str(url))
            item = SoccerProjItem()
            yield scrapy.Request(url, callback=self.parse_2006_2, meta={'item': item}, dont_filter=True)

        datas4 = response.css(
            'div.repCntAreaBack > div > div table:nth-child(10) tr')
        for data in datas4:
            # result = data.css('td:nth-child(6) a::text').extract()
            url = data.css("td:nth-child(3) a::attr(href)").extract_first()
            # url = data.css("td:nth-child(6) a::text").extract_first()
            # url = data.css("td:nth-child(6) a::attr(href)").extract_first()
            if not url:
                continue
            url = response.urljoin(url)
            print("url ========== " + str(url))
            item = SoccerProjItem()
            yield scrapy.Request(url, callback=self.parse_2006_2, meta={'item': item}, dont_filter=True)

    def parse_2006_2(self, response):
        item = response.meta['item']
        temp = response.css(
            'div.repCntAreaBack div td span::text').extract()
        print("temp ========= " + temp[1])
        item['year'] = "20" + re.search("[0-9]+", temp[1]).group()
        month = re.search("..\.[0-9]+", temp[1]).group()
        # print("month = " + month)
        item['month'] = re.sub('..\.', '', month)
        day = re.search("..\...\.[0-9]+", temp[1]).group()
        item['day'] = re.sub('..\...\.', '', day)
        item['leagu_name'] = response.css(
            'div.repCntAreaBack div p:nth-child(2) > img::attr(alt)').extract_first()
        item['team_home'] = response.css(
            'div.repCntAreaBack table td p::text').extract()[2]
        item['team_away'] = response.css(
            'div.repCntAreaBack table td p::text').extract()[-1]
        item['results_home'] = response.css(
            'p.tokuten::text').extract()[0]
        item['results_away'] = response.css(
            'p.tokuten::text').extract()[1]
        goal_home = response.css(
            'div.repCntAreaBack tr:nth-child(3) > td:nth-child(1) span.s125::text').extract()
        if goal_home:
            goal_home = list(map(lambda x: x.strip(), goal_home))
            item['goal_home'] = goal_home
        goal_away = response.css(
            'div.repCntAreaBack tr:nth-child(3) > td:nth-child(3) span.s125::text').extract()
        if goal_away:
            goal_away = list(map(lambda x: x.strip(), goal_away))
            item['goal_away'] = goal_away
        item['time'] = []
        item['url'] = response.url
        for elem in item['goal_home']:
            temp = re.findall('.*分', elem)
            temp = " ".join(temp).strip()
            if temp:
                item['time'].append(temp)
            else:
                continue

        for elem in item['goal_away']:
            temp = re.findall('.*分', elem)
            temp = " ".join(temp).strip()
            if temp:
                item['time'].append(temp)
            else:
                continue
        # item['id'] =
        yield item
# contentsArea > div > table:nth-child(4) > tbody > tr > td:nth-child(3) > div.repCntAreaBack > div > div > table:nth-child(6) > tbody > tr:nth-child(2) > td:nth-child(3) > span > a
# contentsArea > div > table:nth-child(4) > tbody > tr > td:nth-child(3) > div.repCntAreaBack > div > div > table:nth-child(10) > tbody > tr:nth-child(2) > td:nth-child(3) > span > a
# contentsArea > div > table:nth-child(4) > tbody > tr > td:nth-child(3) > div.repCntAreaBack > div > div > table:nth-child(10) > tbody > tr:nth-child(3) > td:nth-child(3) > span > a
# div.repCntAreaBack > div > div > table > tbody > tr > td > p > span

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

#  実行時CSVに書き出す場合はーーーーー　scrapy crawl SoccerSpider -o results/soccer.csv
