# -*- coding: utf-8 -*-
import time

import scrapy
from pyquery import PyQuery as pq

from news_spider import items


class HenanSpider(scrapy.Spider):
    name = 'henan'
    base_url = 'http://www.henan.gov.cn'
    next_page_template = "https://www.henan.gov.cn/ywdt/hnyw/index_%s.html"
    allowed_domains = [base_url]
    start_urls = ['https://www.henan.gov.cn/ywdt/hnyw/index_999.html']

    def parse(self, response):
        html = pq(str(response.body, encoding='utf-8'), parser='html')
        for a in html('.mt15 li a'):
            url = a.attrib['href']
            yield scrapy.Request(url=url,
                                 meta={
                                     'url': url,
                                     "id": url,
                                     'title': a.text,
                                     'tag': 'henan'
                                 },
                                 callback=self.parse_detail,
                                 dont_filter=True)

        next_page = self.parse_next_pate(html)
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        html = pq(str(response.body, encoding='utf-8'), parser='html')

        item = items.JiangSuNewsSpiderItem()
        item['id'] = response.meta['id']
        item['tag'] = response.meta['tag']
        item['category'] = 'gov'
        item['title'] = response.meta['title']
        item['publish_time'] = time.strptime(html('#pubDate').text().strip(), "%Y-%m-%d %H:%M") if html('#pubDate').text().strip() else None
        item['content'] = html('#content').text()
        yield item

    @staticmethod
    def parse_next_pate(html):
        next_page = html('.sDisable:contains("下一页")')
        print(next_page)
        return None if next_page.attr('onclick') is None else HenanSpider.next_page_template % (
                int(next_page.attr('data-page')) - 1)
