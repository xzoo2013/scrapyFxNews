#-*-coding:utf-8-*-

from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from crawlfx168.items import Crawlfx168Item
from datetime import date,time,datetime
import pymongo
from scrapy.log import ScrapyFileLogObserver
import logging
#from scrapy.conf import settings

class Crwalfx168Spider(CrawlSpider):
    name = 'crawlfxspider_all'
 
    allowed_domains = ['news.fx168.com']
    start_urls = ["http://news.fx168.com/all/list_1.shtml"]

    rules = (
        Rule(SgmlLinkExtractor(allow=['http://news.fx168.com/.*\.shtml'],restrict_xpaths=("//div[@id='divNewslist']")), callback="parse_news"),
        Rule(SgmlLinkExtractor(allow=['http://news\.fx168\.com/all/list_[2-4]\.shtml']))# rule for the pager###|http://news\.fx168\.com/all/list_1[0-2]\.shtml'
             )###

 
    def parse_news(self, response):

    	hxs = HtmlXPathSelector(response)
        item = Crawlfx168Item()
        # Extract url
        item['url']=response.url
        # Extract title
        item['title'] = hxs.select("//div[@class='ascout_article_articletitle']/h1/text()").extract()[0] # XPath selector for title
       
        #Extract content
        content_list=hxs.select("//div[@class='ascout_article_articlecon']/div[@class='WordSection1']/p/span/text()").extract()
        if content_list==[]:
            content_list=hxs.select("//div[@class='ascout_article_articlecon']//p[@class='MsoNormal']/span/text()").extract()
        if content_list==[]:
            content_list=hxs.select("//div[@class='ascout_article_articlecon']/p/text()").extract()
        content_list2=[]
        for word in content_list:
            content_list2.append("".join(word.split()))
            item['content']="".join(content_list2)
        #Extract isShortMes
        if item["content"]==[]:
            item["content"]="null"
            
        content_str=item['content']
        if len(content_str)<40:#we assume that the len of the  content for a short news is less than 30 char
            item['isShortMes']=1
        else:
            item['isShortMes']=0
        
        #Extract tags
        item['tag'] = hxs.select("//div[@class='ascout_article_articletag']/ul/li/a/text()").extract()# Xpath selector for tag(s)
        tag_list=hxs.select("//div[@class='yjl_article_tongyong_pTag']/b/a/text()").extract()
        item['tag'].extend(tag_list)
        #Extract date
        time_string=hxs.select("//div[@class='ascout_article_articletimewap']/div[@class='ascout_article_articletime']/text()").extract()[0]
        mydate=time_string.split()[0]
        year=int(mydate[0:4])
        month=int(mydate[5:7])
        day=int(mydate[8:10])
        mytime=time_string.split()[1]
        hour=int(mytime[0:2])
        minite=int(mytime[3:5])
        item['year']=year
        item['month']=month
        item['day']=day
        item['hour']=hour
        item['minite']=minite
        item['second']=0
        item['dtime']=datetime(year,month,day,hour,minite)
        
        return item   
