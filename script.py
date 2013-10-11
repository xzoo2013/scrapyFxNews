#!/usr/bin/python2.7
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from crawlfx168.spiders.crawlfx_all import Crwalfx168Spider
import scrapy.settings

spider = Crwalfx168Spider()
settings = scrapy.settings.CrawlerSettings()
settings.overrides['DOWNLOAD_DELAY'] = 0.25
settings.overrides['MONGODB_SERVER'] = "localhost"
settings.overrides['MONGODB_PORT'] = 27017
settings.overrides['MONGODB_DB'] = "fx_db"
settings.overrides['MONGODB_COLLECTION'] = "fx_news_headline"
settings.overrides['MONGODB_COLLECTION_1'] = "fx_news_all"
settings.overrides['COOKIES_ENABLED'] = False
settings.overrides['ITEM_PIPELINES'] = ['crawlfx168.pipelines.DuplicatesPipeline','crawlfx168.pipelines.MongoDBPipeline_all']



crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run() # the script will block here until the spider_closed signal was sent
# settings = scrapy.settings.CrawlerSettings()
# settings.overrides['DOWNLOAD_TIMEOUT'] = 30
# crawler = CrawlerProcess(settings)
# crawler.install()
# crawler.configure()
