# -*- coding: utf-8 -*-
import scrapy


class ReportsSpider(scrapy.Spider):
    name = "reports"
    start_urls = [
        'http://www.chinaventure.com.cn/cmsmodel/report/list.shtml',
    ]

    def parse(self, response):
        pages = response.css('li div.t_01 a::attr(href)').extract()
        for page in pages:
            yield scrapy.Request(response.urljoin(page), callback=self.parse_page)

    def parse_page(self, response):
        article = response.css('div.left_02').extract_first()
        title = response.css('div.left_02 h1.h1_01::attr(title)').extract_first()
        author = response.css('div.left_02 div.details_01_l span::text').extract_first()
        time_pub = response.css('div.left_02 div.details_01_l span::text')[1].extract()
        content = response.css('div.left_02 div.content_01').extract_first()
        yield {
            # 'raw': article,
            'title': title,
            'author': author,
            'time_pub': time_pub,
            # 'content': content
        }
