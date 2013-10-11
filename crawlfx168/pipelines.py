#-*-coding:utf-8-*-

import pymongo
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from scrapy import log
from datetime import date

class DuplicatesPipeline(object):

    def __init__(self):
        # class variable must start with self. !!!!!!!
        
        self.client=MongoClient('localhost',27017)
        self.db=self.client['fx_db']
        self.collection=self.db['fx_news_all']
        self.latest=self.collection.find({},{"dtime"}).sort([("dtime",pymongo.DESCENDING)]).limit(1)
        self.lastDate=self.latest.next()["dtime"]
        self.bornder=self.collection.find({"dtime":self.lastDate},{"title":1,"_id":0})
        self.titlelist=self.bornder[:]
        self.titles=[]
        for item in self.titlelist:
           # print item["title"]
            self.titles.append(item["title"])
            
        

    def process_item(self, item, spider):
        if item['dtime'] < self.lastDate or item["title"] in set(self.titles):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            return item

class MongoDBPipeline_headline(object):
    def __init__(self):
        self.connection = pymongo.Connection("localhost", 27017)
        self.db = self.connection['fx_db']
        self.collection = self.db['fx_news_headline']
        
    def process_item(self, item, spider):
        if spider.name not in ['crawlfxspider']: 
            return item
        else:
            valid = True
            for data in item:
              # here we only check if the data is not null
              # but we could do any crazy validation we want
              if not data:
                valid = False
                raise DropItem("Missing %s of blogpost from %s" %(data, item['title']))
            if valid:
              self.collection.insert(dict(item))
              log.msg("Item wrote to MongoDB database %s/%s" %
                      ('fx_db','fx_news_headline'),
                      level=log.DEBUG, spider=spider) 
            return item

class MongoDBPipeline_all(object):
    def __init__(self):
        self.connection = pymongo.Connection('localhost',27017)
        self.db =self. connection['fx_db']
        self.collection =self. db['fx_news_all']
        
    def process_item(self, item, spider):
        if spider.name not in ['crawlfxspider_all']: 
            return item
    	valid = True
        for data in item:
          # here we only check if the data is not null
          # but we could do any crazy validation we want
       	  if not data:
            valid = False
            raise DropItem("Missing %s of blogpost from %s" %(data, item['title']))
        if valid:
          self.collection.insert(dict(item))
          log.msg("Item wrote to MongoDB database %s/%s" %
                  ('fx_db', 'fx_news_all'),
                  level=log.DEBUG, spider=spider) 
        return item
