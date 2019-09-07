# -*- coding: utf-8 -*-
import time

import scrapy
from pyquery import PyQuery as pq

from news_spider import items


class HebeiSpider(scrapy.Spider):
    name = 'hebei'
    base_url = 'http://www.hebei.gov.cn'
    allowed_domains = [base_url]
    start_urls = ['http://www.hebei.gov.cn/eportal/ui?pageId=14471750&currentPage=478&moduleId=df829939b783468f8455e0dc04c3b0da']

    def parse(self, response):
        html = pq(str(response.body, encoding='utf-8'), parser='html')
        for a in html('.szf_ejlb_List li a'):
            url = self.base_url + a.attrib['href']
            yield scrapy.Request(url=url,
                                 meta={
                                     'url': self.base_url + url,
                                     "id": url,
                                     'title': a.attrib['title'],
                                     'tag': 'hebei'
                                 },
                                 callback=self.parse_detail,
                                 dont_filter=True)

        next_page = self.parse_next_pate(html)
        if next_page is not None:
            yield scrapy.Request(url=self.base_url + next_page, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        html = pq(str(response.body, encoding='utf-8'), parser='html')

        item = items.JiangSuNewsSpiderItem()
        item['id'] = response.meta['id']
        item['tag'] = response.meta['tag']
        item['category'] = 'gov'
        item['title'] = response.meta['title']
        item['publish_time'] = time.strptime(html('.xl_shijian').text().strip(), "%Y年%m月%d日")
        item['content'] = html('#zoom').text()
        yield item

    @staticmethod
    def parse_next_pate(html):
        next_page = html('.pagingNormal:contains("下一页")')
        return None if len(next_page) == 0 else next_page[0].attrib['tagname']
