# -*- coding: utf-8 -*-
import scrapy
import time
import re


class FinanceScopeSpider(scrapy.Spider):
    name = "finance_scope"
    start_urls = ["http://finance.jrj.com.cn/list/guoneicj.shtml"]

    def parse(self, response):
        pages = response.css('ul.list2 li a::attr(href)').extract()
        for page in pages:
            yield scrapy.Request(page, callback=self.parseDetailPage)

    @classmethod
    def parseDetailPage(cls, response):
        cube = response.css('div.titmain')
        title = cube.css('h1').extract_first()
        intro = cube.css('p.inftop span').extract()
        keyword = cube.css('p.keyword a::text').extract()
        keyword = ",".join(keyword)
        timePub = intro[0]
        # timeStamp = int(time.mktime(time.strptime(timePub, u"%Y年%m月%d日 %H:%M:%S")))
        source = intro[1]
        author = intro[2]
        content = cube.css('div.texttit_m1 p::text').extract()
        content = "\n".join(content)
        # pattern = re.compile('.*start.*')
        # match = pattern.match(title.encode('utf-8'))
        # if match:
        #     title = match.group(1)
        yield {
            'title': title,
            'time_pub': timePub,
            'source': source,
            'author': author,
            'keyword': keyword,
            # 'content': content
        }
