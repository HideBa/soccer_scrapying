# -*- coding: utf-8 -*-
import scrapy
from ..items import SoccerProjItem


class SoccerspiderSpider(scrapy.Spider):
    name = 'SoccerSpider'
    allowed_domains = ['jfa.jp']
    start_urls = [
        'http://www.jfa.jp/match/takamado_jfa_u18_premier2019/east/schedule_result/']

    # def parse(self, response):
    #     print("start -----------")
    #     for item in response.css('div#main-colum div#page-title'):
    #         yield SoccerProjItem(
    #         team_home = item.css('h3::text').extract_first()
    #         )
    #         print("-----------")
    def parse_initialize(self, response):
        start_path = response.css(
            '#sub > div.subMenu > ul > li.local-west_schedule > a::attr(href)').extract_first()
        return start_path

    def parse(self, response):
        # print('666666666666666666666')
        # page2 = response.urljoin(response.css('div.shcedule-tournament a::text')).extract_first()
        # print(page2)
        path = self.parse_initialize(response)
        for topic in response.css('table.table_theme1'):
            item = SoccerProjItem()
            item['headline'] = topic.css('a::text').extract_first()
            print(item['headline'])
            page = topic.css('a::attr(href)').extract_first()
            print("0000000000000000000000000000000")
            print(page)
            yield scrapy.Request(topic.css('a::attr(href)').extract_first(), callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        item['url'] = response.url
        item['team_home'] = response.css(
            'div.score-board-header p::text').extract_first()
        yield item
