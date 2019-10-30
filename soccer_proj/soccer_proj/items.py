# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.exporters import CsvItemExporter


# class SoccerCsvExporter(CsvItemExporter):
#     def serialize_field(self, field, name, value):
#         if field == 'leagu_name':
#             return '$ %s' % str(value)
#         return super(SoccerProjItem, self).serialize_field(field, name, value)


class SoccerProjItem(scrapy.Item):
    leagu_name = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()
    day = scrapy.Field()
    round = scrapy.Field()
    team_home = scrapy.Field()
    team_away = scrapy.Field()
    url = scrapy.Field()
    results_home = scrapy.Field()
    results_away = scrapy.Field()
    goal_home = scrapy.Field()
    goal_away = scrapy.Field()
    time = scrapy.Field()
    player = scrapy.Field()
    id = scrapy.Field()
    # parent_url = scrapy.Field()
