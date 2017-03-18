# -*- coding: utf-8 -*-
import scrapy
import time


class FinanceScopeSpider(scrapy.Spider):
    name = "finance_scope"
    start_urls = [
        "http://finance.jrj.com.cn/list/guoneicj.shtml"
    ]
    # finance.jrj.com.cn 的特征，翻前10页面url格式规律
    for i in range(2, 11):
        start_urls.append(start_urls[0][:-6]+"-"+str(i)+start_urls[0][-6:])

    def parse(self, response):
        pages = response.css('ul.list2 li a::attr(href)').extract()
        for page in pages:
            yield scrapy.Request(page, callback=self.parseDetailPage)

    @classmethod
    def parseDetailPage(cls, response):
        title = "获取失败"
        timePub = ""
        source = ""
        author = ""
        timeStamp = 0

        cube = response.css('div.titmain')
        titleRaw = cube.css('h1::text').extract()
        if len(titleRaw) > 2:
            title = titleRaw[2].strip("\r\n")
        keyword = cube.css('p.keyword a::text').extract()
        keyword = ",".join(keyword).strip("\r\n")
        content = cube.css('div.texttit_m1 p::text').extract()
        content = "\n".join(content)

        intro = cube.css('p.inftop span')
        if len(intro) >= 3:
            timePubRaw = intro[0].css('span::text').extract()
            if len(timePubRaw) > 0:
                timePub = timePubRaw[0].strip("\r\n")
                timeStamp = int(time.mktime(time.strptime(timePub, u"%Y-%m-%d %H:%M:%S")))
            sourceRaw = intro[1].css('span::text').extract()
            if len(sourceRaw) > 1:
                source = sourceRaw[1].strip("\r\n")
            authorRaw = intro[2].css('span::text').extract()
            if len(authorRaw) > 1:
                author = authorRaw[1].strip("\r\n")

        yield {
            'url': response.url,
            'crawler': cls.name,
            'title': title,
            'time_pub': timePub,
            'time_stamp': timeStamp,
            'source': source,
            'author': author,
            'keyword': keyword,
            'content': content
        }
