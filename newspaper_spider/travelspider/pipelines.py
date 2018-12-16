# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class TravelspiderPipeline(object):
    def __init__(self):
        conn = pymongo.MongoClient()
        self.col = conn['newspaper']['ckxx']

    '''处理采集资讯, 存储至Mongodb数据库'''
    def process_item(self, item, spider):
        try:
            self.col.insert(dict(item))
        except (pymongo.errors.WriteError, KeyError) as err:
            raise DropItem("Duplicated Item: {}".format(item['name']))
        return item
