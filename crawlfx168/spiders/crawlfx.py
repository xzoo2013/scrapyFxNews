#-*-coding:utf-8-*-

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from crawlfx168.items import Crawlfx168Item
from datetime import date,time
import pymongo
from scrapy.conf import settings

class Crwalfx168Spider(BaseSpider):
    

    
    # the parameter for the scrapy crawl

    name = 'crawlfxspider'
 
    allowed_domains = ['news.fx168.com']
    start_urls = ['http://news.fx168.com/headline.shtml'] # urls from which the spider will start crawling
    def parse(self,response):
       hxs=HtmlXPathSelector(response)
       for url in hxs.select('//form/div/div/div/ul/li/b/a[@href]/@href').extract():
           print url
           yield Request(url,callback=self.parse_news)
       
    #this is the globle parameter read from the db.parameter collection.
    global num
    num=0
    def parse_news(self, response):
        # make the connection to the database
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        collection = db[settings['MONGODB_COLLECTION']]

    	hxs = HtmlXPathSelector(response)
        item = Crawlfx168Item()
        # Extract url
        item['url']=response.url
        # Extract title
        item['title'] = hxs.select("//div[@class='ascout_article_articletitle']/h1/text()").extract()[0] # XPath selector for title
        # Extract author
        item['tag'] = hxs.select("//div[@class='ascout_article_articletag']/ul/li/a/text()").extract()# Xpath selector for tag(s)
        #Extract content
        content_list=hxs.select("//div[@class='ascout_article_articlecon']/div[@class='WordSection1']/p/span/text()").extract()
        content_list2=[]
        for word in content_list:
            content_list2.append("".join(word.split()))
            item['content']="".join(content_list2)
        #Extract tags
        tag_list=hxs.select("//div[@class='yjl_article_tongyong_pTag']/b/a/text()").extract()
        item['tag'].append(tag_list)
        #Extract date
        time_string=hxs.select("//div[@class='ascout_article_articletimewap']/div[@class='ascout_article_articletime']/text()").extract()[0]
        mydate=time_string.split()[0]
        year=mydate[0:4]
        month=mydate[5:7]
        day=mydate[8:10]
        mytime=time_string.split()[1]
        hour=mytime[0:2]
        minite=mytime[3:5]
        item['date']=[year,month,day]
        item['time']=[hour,minite]
        item['year']=int(year)
        item['month']=int(month)
        item['day']=int(day)
        item['hour']=int(hour)
        item['minite']=int(minite)
        item['second']=0
        

        #Extract id
        global num
        item['news_id']=num
        num=num+1
        return item   
