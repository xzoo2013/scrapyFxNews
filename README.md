scrapyFxNews
============

This project is aimed to collect currency exchange news from the website fx168 with scrapy, 
an open source web crawling framework written in Python

(note: some of the comments are written in Chinese and actually the www.fx168.com is a Chinese financial website)

Functionalities: first crawl across all the target webpages and download the news and then store it in the
MongoDb, a document-oriented database

Basically the project is following the structure of Scrapy:

first create the Item() class which defines contents to be collected

Second create the spider class which realize the process of content grabbing

third create the pipeline class which define the way data is stored

In the end , I want to mention that I have set the grabing tast as a routine in my linux system, using the crontab
which you can google and then know  how to use this powerful task schedule tool.

And the codes to run the spider from script is listed in the script.py

This project works very well on my computer, have fun!
