# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import requests
import os
from tpmsg import settings


class TpmsgPipeline(object):

    def __init__(self):
        self.file = codecs.open('tupu.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class ImageDownloadPipline(object):

    def process_item(self, item, spider):
        if 'pic_uri' in item:
            i = 0
            dir_path = '%s/%s' % (settings.IMAGES_STORE, item['title'])
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for each in item['pic_uri']:
                hz = each[-4:]
                file_path = dir_path + '/' + str(i) + hz
                try:
                    pic = requests.get(each, stream=True)
                except requests.exceptions.ConnectionError:
                    print('当前图片无法下载')
                    continue
                fp = open(file_path, 'wb')
                fp.write(pic.content)
                fp.close()
                i += 1
        return item
