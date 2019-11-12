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
        datas = response.css(
            'div.repCntAreaBack > div > div > table tr')
        count = 0
        for data in datas:
            count += 1
            print("data=================" + str(data.css("::text")))
            year = data.css('td:nth-child(1) span::text').extract_first()
            result = data.css('td:nth-child(3) span a::text').extract()
            print("year===" + str(year))
            if re.search("[0-9]", str(year)):
                item = SoccerProjItem()
                year = '20' + re.search('[0-9]+', year).group()
                item['year'] = year
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
                item['round'] = response.css(
                    'div.repCntAreaBack > div > div > div > p > span > span::text').extract_first().strip('　試合スケジュール')
                url = data.css(
                    "td:nth-child(3) span a::attr(href)").extract_first()
                url = response.urljoin(url)
                item['url'] = url
                id = re.search('M[0-9]{2}', item['url']).group().lstrip('M')
                item['id'] = id
                print("id============" + id)
                item['leagu_name'] = "高円宮杯 第18回全日本ユース（U-15）サッカー選手権大会"
                # item['goal_home'] = []
                # item['goal_away'] = []
            # elif year == '得点者':
            #     goal_players = data.css(
            #         'td:nth-child(2) div::text').extract()
            #     goal_players = list(map(lambda x: x.strip(), goal_players))
            #     goal_players = list(filter(lambda x: x != "", goal_players))
            #     print("goal_list===" + str(goal_players))
            #     for player in goal_players:
            #         if player[0] in item['team_home']:
            #             player = player[2:]
            #             minute = re.findall('[0-9]+分', player)
            #             print('minute============-' + str(minute))
            #             player = re.search('.+\(', player).group()
            #             player = player.rstrip('(')
            #             if len(minute) > 1:
            #                 for elem in minute:
            #                     goal_home = elem + player
            #                     item['goal_home'].append(goal_home)
            #             else:
            #                 print("player======" + str(player))
            #                 print("minute=======" + str(minute))
            #                 goal_home = str(minute) + player
            #                 item['goal_home'].append(goal_home)
            #         elif player[0] in item['team_away']:
            #             player = player[2:]
            #             minute = re.search('[0-9]+分\)', player).group()
            #             player = re.search('.+\(', player).group()
            #             player = player.rstrip('(')
            #             minute = minute.rstrip(')')
            #             print("player======" + str(player))
            #             print("minute=======" + str(minute))
            #             goal_away = minute + player
            #             item['goal_away'].append(goal_away)
            #     item['time'] = []

            #     for elem in item['goal_home']:
            #         temp = re.findall('.*分', elem)
            #         temp = " ".join(temp).strip()
            #         if temp:
            #             item['time'].append(temp)
            #         else:
            #             continue

            #     for elem in item['goal_away']:
            #         temp = re.findall('.*分', elem)
            #         temp = " ".join(temp).strip()
            #         if temp:
            #             item['time'].append(temp)
            #         else:
            #             continue
            else:
                continue

            # if count % 2 != 0:
            yield item

    def parse_round_2(self, response):
        datas = response.css(
            'div.repCntAreaBack > div > div > table tr')
        count = 0
        for data in datas:
            count += 1
            print("data=================" + str(data.css("::text")))
            year = data.css('td:nth-child(1) span::text').extract_first()
            result = data.css('td:nth-child(4) span a::text').extract()
            print("year===" + str(year))
            if re.search("[0-9]", str(year)):
                item = SoccerProjItem()
                year = '20' + re.search('[0-9]+', year).group()
                item['year'] = year
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
                item['round'] = response.css(
                    'div.repCntAreaBack > div > div > div > p > span > span::text').extract_first().strip('　試合スケジュール')
                result = data.css('td:nth-child(4) span a::text').extract()
                print("result============" + str(result))
                item['results_home'] = re.search('[0-9]+', result[0]).group()
                item['results_away'] = re.search(
                    '\-[0-9]+', result[0]).group().replace("-", "")
                url = data.css(
                    "td:nth-child(4) span a::attr(href)").extract_first()
                url = response.urljoin(url)
                item['url'] = url
                id = re.search('M[0-9]{2}', item['url']).group().lstrip('M')
                item['id'] = id

                item['leagu_name'] = "高円宮杯 第18回全日本ユース（U-15）サッカー選手権大会"
                # item['goal_home'] = []
                # item['goal_away'] = []
            # elif year == '得点者':
            #     goal_players = data.css(
            #         'td:nth-child(2) div::text').extract()
            #     goal_players = list(map(lambda x: x.strip(), goal_players))
            #     goal_players = list(filter(lambda x: x != "", goal_players))
            #     print("goal_list===" + str(goal_players))
            #     for player in goal_players:
            #         if player[0] in item['team_home']:
            #             player = player[2:]
            #             minute = re.findall('[0-9]+分', player)
            #             print('minute============-' + str(minute))
            #             player = re.search('.+\(', player).group()
            #             player = player.rstrip('(')
            #             if len(minute) > 1:
            #                 for elem in minute:
            #                     goal_home = elem + player
            #                     item['goal_home'].append(goal_home)
            #             else:
            #                 print("player======" + str(player))
            #                 print("minute=======" + str(minute))
            #                 goal_home = str(minute) + player
            #                 item['goal_home'].append(goal_home)
            #         elif player[0] in item['team_away']:
            #             player = player[2:]
            #             minute = re.search('[0-9]+分\)', player).group()
            #             player = re.search('.+\(', player).group()
            #             player = player.rstrip('(')
            #             minute = minute.rstrip(')')
            #             print("player======" + str(player))
            #             print("minute=======" + str(minute))
            #             goal_away = minute + player
            #             item['goal_away'].append(goal_away)
            #     item['time'] = []

                # for elem in item['goal_home']:
                #     temp = re.findall('.*分', elem)
                #     temp = " ".join(temp).strip()
                #     if temp:
                #         item['time'].append(temp)
                #     else:
                #         continue

                # for elem in item['goal_away']:
                #     temp = re.findall('.*分', elem)
                #     temp = " ".join(temp).strip()
                #     if temp:
                #         item['time'].append(temp)
                #     else:
                #         continue
            else:
                continue

            # if count % 2 != 0:
            yield item

    def closed(self, response):
        selenium_close()

    # def parse(self, response):
    #     pass
