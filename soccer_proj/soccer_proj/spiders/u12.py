# -*- coding: utf-8 -*-
import scrapy


class U12Spider(scrapy.Spider):
    name = 'u12'
    allowed_domains = ['http://www.jfa.jp/match/japan_u12_football_championship_2019/']
    start_urls = ['http://http://www.jfa.jp/match/japan_u12_football_championship_2019//']

    def parse(self, response):
        pass
