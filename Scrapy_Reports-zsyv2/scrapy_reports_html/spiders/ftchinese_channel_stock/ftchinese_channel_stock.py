# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy_reports_html.utils import data_maintain_util
from scrapy_reports_html import items


class ftchinese_channel_stock(scrapy.Spider):
    name = "ftchinese_channel_stock"
    start_urls = [
        "http://www.ftchinese.com/channel/stock.html?page=1"
    ]
    # ftchinese.com.channel的特征，翻前10页面url格式规律
    for i in range(2, 11):
 #       start_urls.append(start_urls[0][:-1]+"-"+str(i)+start_urls[0][-6:])
        start_urls.append("http://www.ftchinese.com/channel/stock.html?page=" + str(i))

    def parse(self, response):
        pages = response.css('div.item-inner a::attr(href)').extract()

        for page in pages:
            # 先判断是否爬过这个详情url了
            if data_maintain_util.DataMaintainUtil.isUrlExist(page):
                continue
            else:
                yield scrapy.Request("http://www.ftchinese.com/"+page, callback=self.parseDetailPage)

    @classmethod
    def parseDetailPage(cls, response):
        item = items.ScrapyReportsHtmlItem()
        title = "获取失败"
        timePub = ""
        source = ""
        author = ""
        timeStamp = 0

        #cube = response.css('div.story-theme')
        title = response.css('.story-headline::text').extract()
       # if len(titleRaw) > 2:
       #     title = titleRaw[2].strip("\r\n")
       #keyword = cube.css('p.keyword a::text').extract()
       #keyword = ",".join(keyword).strip("\r\n")
        abstract = response.css('.story-lead::text').extract()
        content = response.css('.story-body  p::text').extract()
        content = "\n".join(content)

        intro = response.css('.story-time')
        timeRaw = response.css('.story-time::text').extract_first()
        time = timeRaw.split("更新于")[1]
        # if len(intro) >= 3:
        #     timePubRaw = intro[0].css('span::text').extract()
        #     if len(timePubRaw) > 0:
        #         timePub = timePubRaw[0].strip("\r\n")
        #         timeStamp = int(time.mktime(time.strptime(timePub, u"%Y-%m-%d %H:%M:%S")))
        #     sourceRaw = intro[1].css('span::text').extract()
        #     if len(sourceRaw) > 1:
        #         source = sourceRaw[1].strip("\r\n")
        #     authorRaw = intro[2].css('span::text').extract()
        #     if len(authorRaw) > 1:
        #         author = authorRaw[1].strip("\r\n")
        item['title'] = title
        item['abstract'] = abstract
        item['content'] = content
        item['time'] = time

        yield item
            # 'url': response.url,
            # 'crawler': cls.name,
            # 'title': title,
            # 'time_pub': time,
            # # 'time_stamp': timeStamp,
            # 'source': source,
            # 'author': author,
            # # 'keyword': keyword,
            # 'abstract': abstract,
            # 'content': content


