# Scrapy settings for crawlfx168 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawlfx168'

SPIDER_MODULES = ['crawlfx168.spiders']
NEWSPIDER_MODULE = 'crawlfx168.spiders'


ITEM_PIPELINES = ['crawlfx168.pipelines.DuplicatesPipeline','crawlfx168.pipelines.MongoDBPipeline_all']###,'crawlfx168.pipelines.MongoDBPipeline_headline'


MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "fx_db"
MONGODB_COLLECTION = "fx_news_headline"
MONGODB_COLLECTION_1 = "fx_news_all"



COOKIES_ENABLED = False

DOWNLOAD_DELAY = 0.25
