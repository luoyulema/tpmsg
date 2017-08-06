# -*- coding: utf-8 -*-
import scrapy
# from scrapy.spider import CrawlSpider, Rule
# from scrapy.linkextractor import Linkextractor
from scrapy.http import Request
from bs4 import BeautifulSoup
from tpmsg.items import TpmsgItem
import logging


class TupuSpider(scrapy.Spider):
    name = 'tupu'
    allowed_domains = ['tpmsg.com']
    start_urls = ['http://www.tpmsg.com/index.php/category/jpmx']

    def start_requests(self):
        uri = 'http://www.tpmsg.com/index.php/category/jpmx/page/'
        for i in range(1, 2):
            url = uri + str(i)
            yield Request(url=url, callback=self.parse_page1)

    def parse_page1(self, response):
        self.logger.info('parse url:%s', response.url)
        # item = TpmsgItmm()
        # //*[@id = "post_container"] / li[7] / div / div[1] / a
        soup = BeautifulSoup(response.body, 'lxml')
        for bumb in soup.find_all('a', class_='zoom'):
            # item['numb_uri']=bumb['href']
            yield Request(url=bumb['href'], callback=self.parse_page2)

    def parse_page2(self, response):
        self.logger.info('parse on:%s', response.url)
        item = TpmsgItem()
        soup = BeautifulSoup(response.body, 'lxml')
        item['title'] = soup.find('h1').string
        pics = []
        for pic in soup.find_all('a', class_='pirobox_gall'):
            pics.append(pic['href'])
            item['pic_uri'] = pics

        return item
