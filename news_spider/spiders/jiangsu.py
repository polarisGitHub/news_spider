# -*- coding: utf-8 -*-
import time

import scrapy
from pyquery import PyQuery as pq

from news_spider import items
import logging


class JiangsuSpider(scrapy.Spider):
    name = "jiangsu"
    base_url = "http://www.jiangsu.gov.cn"
    allowed_domains = [base_url]
    start_urls = ['http://www.jiangsu.gov.cn/col/col60096/index.html?uid=212860&pageNum=73']

    def parse(self, response):
        html = pq(str(response.body, encoding='utf-8'), parser='html')
        for a in html('.main_list a'):
            url = self.base_url + a.attrib['href']
            yield scrapy.Request(url=url,
                                 meta={'url': url, "id": url.split("/")[-1], 'title': a.text, 'tag': 'jiangsu'},
                                 callback=self.parse_detail,
                                 dont_filter=True)

        next_page = self.parse_next_pate(html)
        if next_page is not None:
            url = self.base_url + next_page
            logging.info("spider:" + url)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        html = pq(str(response.body, encoding='utf-8'), parser='html')

        contents = []
        for i in html('#zoom p'):
            if i.text is not None:
                contents.append(i.text)

        item = items.JiangSuNewsSpiderItem()
        item['id'] = response.meta['id']
        item['tag'] = response.meta['tag']
        item['category'] = 'gov'
        item['title'] = response.meta['title']
        publish_time = html('.sp_time font')[0].text.split("：")[1]
        item['publish_time'] = time.strptime(publish_time, "%Y-%m-%d %H:%M") if publish_time else None
        item['content'] = '\n'.join(contents)
        yield item

    @staticmethod
    def parse_next_pate(html):
        return html('.default_pgNext:not(.default_pgNextDisabled)').attr("href")
