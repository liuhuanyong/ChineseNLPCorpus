# coding=utf-8
import scrapy
import pymongo
from lxml import etree
from travelspider.items import TravelspiderItem
import os
import datetime

class BuildData:
    def __init__(self):
        self.date_list = self.create_dates()
        return
    '''get dates between two date'''
    def get_dates(self, start, end):
        date_start = datetime.datetime.strptime(start, '%Y-%m-%d')
        date_end = datetime.datetime.strptime(end, '%Y-%m-%d')
        date_list = []
        while date_start < date_end:
            date_start += datetime.timedelta(days=1)
            qu = date_start.strftime('%Y-%m-%d')
            date_list.append(qu)
        return date_list

    def create_dates(self):
        date_list = self.get_dates('1957-02-28', '2002-12-31')
        return date_list

class TravelSpider(scrapy.Spider):
    name = 'travel'
    '''资讯采集主控函数'''
    def start_requests(self):
        Data = BuildData()
        date_list = Data.create_dates()
        for date in date_list:
            print(date)
            date_url = 'http://www.laoziliao.net/ckxx/%s'%date
            param = {'url': date_url, 'date': date}
            yield scrapy.Request(url=date_url, meta=param, callback=self.get_urllist, dont_filter=True)

    '''get_urllist'''
    def get_urllist(self, response):
        selector = etree.HTML(response.text)
        date_url = response.meta['url']
        urls = [i.split('#')[0] for i in selector.xpath('//ul/li/a/@href') if date_url in i]
        for url in set(urls):
            param = {'url':url , 'date': response.meta['date']}
            yield scrapy.Request(url=url, meta=param, callback=self.page_parser, dont_filter=True)

    '''网页解析'''
    def page_parser(self, response):
        selector = etree.HTML(response.text)
        articles = selector.xpath('//div[@class="article"]')
        titles = selector.xpath('//h2/text()')
        contents = []
        for article in articles:
            content = article.xpath('string(.)')
            contents.append(content)
        papers = zip(titles, contents)
        for i in papers:
            item = TravelspiderItem()
            item['url'] = response.meta['url']
            item['date'] = response.meta['date']
            item['title'] = i[0]
            item['content'] = i[1] 
            yield item
        return
