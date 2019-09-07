# -*- coding: utf-8 -*-
import time

import scrapy
from pyquery import PyQuery as pq

from news_spider import items
import logging


class SichuanSpider(scrapy.Spider):
    name = 'sichuan'
    base_url = 'http://www.sc.gov.cn'
    allowed_domains = [base_url]
    news_url_base = 'http://www.sc.gov.cn/10462/10464/10797/'
    start_urls = [news_url_base + 'jrsc_list.shtml']

    def parse(self, response):
        html = pq(str(response.body, encoding='utf-8'), parser='html')
        for a in html('#dash-table a'):
            url = self.base_url + a.attrib['href']
            yield scrapy.Request(url=url,
                                 meta={
                                     'url': url,
                                     "id": url.split("/")[-1],
                                     'title': a.attrib['title'],
                                     'tag': 'sichuan'
                                 },
                                 callback=self.parse_detail,
                                 dont_filter=True)

        next_page = self.parse_next_pate(html)
        if next_page is not None:
            url = self.news_url_base + '/' + next_page
            logging.info("spider:" + url)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        html = pq(str(response.body, encoding='utf-8'), parser='html')

        contents = []
        for i in html('.cmsArticleContent p'):
            if i is not None and i.text is not None:
                contents.append(i.text)

        item = items.JiangSuNewsSpiderItem()
        item['id'] = response.meta['id']
        item['tag'] = response.meta['tag']
        item['category'] = 'gov'
        item['title'] = response.meta['title']
        publish_time = html('#articleattribute li')[0].text.strip()
        item['publish_time'] = time.strptime(publish_time, "%Y年%m月%d日 %H时%M分") if publish_time else None
        item['content'] = '\n'.join(contents)
        yield item

    @staticmethod
    def parse_next_pate(html):
        next_page = html('#page_div .arrow a:contains("下页")')
        return None if len(next_page) == 0 else next_page[0].attrib['href']
