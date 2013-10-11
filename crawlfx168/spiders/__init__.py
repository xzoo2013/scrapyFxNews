# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import logging
from scrapy.log import ScrapyFileLogObserver
import datetime
localtime=datetime.datetime.now().strftime("%H:%M:%S_%d-%m-%Y")

logfile = open('/home/xiezhe/Desktop/Document/crawlfx168/log_'+localtime+'.log', 'w')
log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
log_observer.start()










