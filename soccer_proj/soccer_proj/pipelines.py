# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exporters import CsvItemExporter
# from .items import SoccerProjItem, SoccerCsvExporter
from .items import SoccerProjItem
from scrapy import signals


# class SoccerCsvExporter(CsvItemExporter):
#     def serialize_field(self, field, name, value):
#         if field == 'leagu_name':
#             return '$ %s' % str(value)
#         return super(SoccerProjItem, self).serialize_field(field, name, value)

# --------------------------------------------------------------
class SoccerProjPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('results_all/%s_result.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        # self.exporter = SoccerCsvExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
# --------------------------------------------------------------------
# def open_spider(self, spider):
#     self.leagu_name_to_exporter = {}

# def close_spider(self, spider):
#     for exporter in self.leagu_name_to_exporter.values():
#         exporter.finish_exporting()
#         exporter.file.close()

# def _exporter_for_item(self, item):
#     leagu_name = item['leagu_name']
#     if leagu_name not in self.leagu_name_to_exporter:
#         f = open('results_all/results_all.csv'.format(leagu_name), 'wb')
#         exporter = SoccerCsvExporter(f)
#         exporter.start_exporting()
#         self.leagu_name_to_exporter[leagu_name] = exporter
#     return self.leagu_name_to_exporter[leagu_name]

# def process_item(self, item, spider):
#     exporter = self._exporter_for_item(item)
#     exporter.export_item(item)
#     return item
