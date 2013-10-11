scrapyFxNews
============

This project is for currency exchange news collection from the website fx168 with the help of scrapy, 
an open source web crawling framework written in Python
(note: some of the comments are written in Chinese and actually the www.fx168.com is a Chinese financial website)

What the project does is pretty simple: first crawl across all the target webpages and download the news and then store it in the
mongodb database 

Basically the project is following the structure of Scrapy:
first define the Item() class which means what contents should be collected

then write the spider class which realises the process of how content should be grabed

then the pipeline class which define the way data is stored

In the end , I want to mention that I have set the grabing tast as a routine in my linux system, using the crontab
you can google it about how to use this powerful task schedule tool.

And the code to run the spider from script is listed in the script.py

This project works very well on my computer, have fun!
