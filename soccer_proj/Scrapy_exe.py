from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from soccer_proj.spiders.SoccerSpider import SoccerspiderSpider
from soccer_proj.spiders.u15 import U15Spider
from soccer_proj.spiders.u12 import U12Spider
from scrapy.crawler import CrawlerProcess

settings = get_project_settings()
# settings.set('FEED_URI', 'results_all/all_results.csv')
settings.set('FEED_URI', 'results/results_2013_2011.csv')
# settings.set('FEED_URI', 'results_all/%(filename)s.csv')

# 複数スパイダー実行用ーーーーーーーーーーーーーーーーーーーーーーー
# configure_logging()
# # runner = CrawlerRunner()
# runner = CrawlerRunner(settings)


# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(SoccerspiderSpider, filename='U18')
#     yield runner.crawl(U15Spider)
#     yield runner.crawl(U12Spider)
#     reactor.stop()


# crawl()
# reactor.run()

# ここまでーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

# 以下単独スパイダー実行用ーーーーーーーーーーーーーーー
process = CrawlerProcess(get_project_settings())

# process.crawl('SoccerSpider')
# process.start()
process.crawl('u15')
process.start()
# process.crawl('u12')
# process.start()
