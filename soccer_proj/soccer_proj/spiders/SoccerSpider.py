# -*- coding: utf-8 -*-
import scrapy
import pprint
from ..items import SoccerProjItem
from ..selenium_middleware import *
# from sclapy_selenium import SeleniumRequest

# yield SeleniumRequest(url=url, callback=self.parse_result)


class SoccerspiderSpider(scrapy.Spider):
    name = 'SoccerSpider'
    allowed_domains = ['jfa.jp']
    start_urls = [
        'http://www.jfa.jp/match/takamado_jfa_u18_premier2019/east/schedule_result/']

    custom_setting = {
        "DOWNLOAD_MIDDLEWARE": {
            "scrapy_list.selenium_middleware.ScrapyListSpiderMiddleware"
        },
        "DOWNLOAD_DELAY": 1.0,
    }

    def start_requests(self):
        # ここに取得したい試合結果一覧のURLをかく
        url = "http://www.jfa.jp/match/takamado_jfa_u18_premier2019/east/schedule_result/"
        # ここで、ブラウザを起動してページを開く
        selenium_get(url)
        # get_aで各試合の詳細URLのa要素を取得
        alist = get_a('li.score a')
        # for文を回してそれぞれのhref属性を取得
        for a in alist:
            page = a.get_attribute('href')
            # それぞれのURLにおいてScrapyRequestを生成
            yield scrapy.Request(page, callback=self.parse)

    def parse(self, response):
        print('response====================' + str(response))
        item = SoccerProjItem()
        item['leagu_name'] = response.css(
            '#ttl_sp > img::attr(alt)').extract_first()
        # いったんHeadlineとして値を取得しているが、ここから後は正規表現だの、Splitみたいなので不要な文字列を削って出力すればよし
        item['round'] = response.css(
            '#inner-header-score > div.text-schedule::text').extract_first()
        item['team_home'] = response.css(
            '#score-board-header > div:nth-child(1) > p:nth-child(2)::text').extract_first()
        item['team_away'] = response.css(
            '#score-board-header > div:nth-child(5) > p:nth-child(2)::text').extract_first()
        item['url'] = response.url
        item['results_home'] = response.css(
            '#score-board-header > div:nth-child(2)::text').extract_first()
        yield item

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
