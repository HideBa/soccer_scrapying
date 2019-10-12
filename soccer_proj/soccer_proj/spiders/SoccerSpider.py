# -*- coding: utf-8 -*-
import scrapy
from ..items import SoccerProjItem

class SoccerspiderSpider(scrapy.Spider):
    name = 'SoccerSpider'
    allowed_domains = ['jfa.jp']
    start_urls = ['http://www.jfa.jp/match/takamado_jfa_u18_premier2019/east/schedule_result/']

    # def parse(self, response):
    #     print("start -----------")
    #     for item in response.css('div#main-colum div#page-title'):
    #         yield SoccerProjItem(
    #         team_home = item.css('h3::text').extract_first()
    #         )
    #         print("-----------")

    def parse(self, response):
        print("start ----------")
        for item in response.css('table.table_theme1 tbody tr.end td'):
            yield SoccerProjItem(
            team_home = item.css('li::text').extract_first()
            )
            print("-----------")



    # def parse(self, response):
    #     print("start scrapy --------------")
    #     for soccer in response.css('div.shcedule-tournament'):
    #         item = SoccerProjItem()
    #         item['team_home'] = soccer.css('div.trigger-tournament::text')
    #         yield item

    