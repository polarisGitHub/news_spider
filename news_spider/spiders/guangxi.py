# -*- coding: utf-8 -*-
import logging

import time
import scrapy
from pyquery import PyQuery as pq

from news_spider import items


class GuangxiSpider(scrapy.Spider):
    name = 'guangxi'
    base_url = 'http://www.gxzf.gov.cn'
    allowed_domains = [base_url]
    start_urls = ['http://www.gxzf.gov.cn/gxyw/index.shtml']

    def parse(self, response):
        html = pq(str(response.body, encoding='utf-8'), parser='html')
        for a in html('.more li a'):
            url = a.attrib['href']
            yield scrapy.Request(url=url,
                                 meta={
                                     'url': url,
                                     "id": url.split("/")[-1],
                                     'title': a.attrib['title'],
                                     'tag': 'guangxi'
                                 },
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
        for i in html('.article-con p'):
            if i is not None and i.text is not None:
                contents.append(i.text)

        item = items.JiangSuNewsSpiderItem()
        item['id'] = response.meta['id']
        item['tag'] = response.meta['tag']
        item['category'] = 'gov'
        item['title'] = response.meta['title']
        publish_time = list(map(lambda x: x.strip(), html('.article-inf-left').text().split(" ")))
        publish_time = ' '.join(publish_time[:-1])
        item['publish_time'] = time.strptime(publish_time, "%Y-%m-%d %H:%M") if publish_time else None
        item['content'] = '\n'.join(contents)
        yield item

    @staticmethod
    def parse_next_pate(html):
        next_page = html('.more-page a:contains("下一页")')
        return None if len(next_page) == 0 else next_page[0].attrib['href']
