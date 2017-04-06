# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy_reports_html.utils import data_maintain_util


class ReportsSpider(scrapy.Spider):
    name = "chinaventure"
    start_urls = [
        'http://www.chinaventure.com.cn/cmsmodel/report/list.shtml',
    ]

    def parse(self, response):
        pages = response.css('li div.t_01 a::attr(href)').extract()
        for page in pages:
            # 先判断是否爬过这个详情url了
            if data_maintain_util.DataMaintainUtil.isUrlExist(page):
                continue
            else:
                yield scrapy.Request(response.urljoin(page), callback=self.parsePage)

    @classmethod
    def parsePage(cls, response):
        title = response.css('div.left_02 h1.h1_01::attr(title)').extract_first()
        author = response.css('div.left_02 div.details_01_l span::text').extract_first()
        time_pub = response.css('div.left_02 div.details_01_l span::text')[1].extract()
        content = response.css('div.left_02 div.content_01').extract_first()

        time_stamp = int(time.mktime(time.strptime(time_pub, u"%Y年%m月%d日 %H:%M:%S")))
        yield {
            'url': response.url,
            'crawler': cls.name,
            'title': title,
            'author': author,
            'time_pub': time_pub,
            'content': content,
            'time_stamp': time_stamp
        }
