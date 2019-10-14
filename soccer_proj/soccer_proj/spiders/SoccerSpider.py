# -*- coding: utf-8 -*-
import scrapy
from ..items import SoccerProjItem


class SoccerspiderSpider(scrapy.Spider):
    name = 'SoccerSpider'
    allowed_domains = ['jfa.jp']
    start_urls = [
        'http://www.jfa.jp/match/takamado_jfa_u18_premier2019/east/schedule_result/']


def parse(self, response):
    for table in response.css('#main-colum > div.section-block > div.shcedule-tournament.js-createSchedule > div:nth-child(1) > div.table-wrap-tournament > table'):
        item = SoccerProjItem()
        item['headline'] = table.xpath(
            '//tbody/tr[1]/td[2]/text()').extract()
        yield item

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
