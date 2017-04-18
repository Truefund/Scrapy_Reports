# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy_reports_html.utils import data_maintain_util
from scrapy_reports_html import items


class yicai_news_markets(scrapy.Spider):
    name = "yicai_news_markets"
    start_urls = [
        "http://www.yicai.com/news/markets/"
    ]
    # ftchinese.com.channel的特征，翻前10页面url格式规律
    #for i in range(2, 11):
 #       start_urls.append(start_urls[0][:-1]+"-"+str(i)+start_urls[0][-6:])
    #    start_urls.append("http://www.ftchinese.com/channel/stock.html?page=" + str(i))

    def parse(self, response):
        pages = response.xpath('//dl[@class="f-cb dl-item"]/dt/a/@href').extract()

        for page in pages:
            # 先判断是否爬过这个详情url了
            if data_maintain_util.DataMaintainUtil.isUrlExist(page):
                continue
            else:
                # add page into mongo db
                yield scrapy.Request(page, callback=self.parseDetailPage)

    @classmethod
    def parseDetailPage(cls, response):
        item = items.ScrapyReportsHtmlItem()
        title = "获取失败"
        timePub = ""
        source = ""
        author = ""
        timeStamp = 0

        #cube = response.css('div.story-theme')
        title = response.css('.f-fs30::text').extract()
       # if len(titleRaw) > 2:
       #     title = titleRaw[2].strip("\r\n")
       #keyword = cube.css('p.keyword a::text').extract()
       #keyword = ",".join(keyword).strip("\r\n")
       # abstract = response.css('.story-lead::text').extract()
        content = response.css('.m-text p::text').extract()
        content = "\n".join(content)

        intro = response.css('.story-time')
        #timeRaw = response.css('.story-time::text').extract_first()
        time = response.css(".m-title ::text").extract()[4]
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
        item['url'] = response.url
        item['title'] = title
        # item['abstract'] = abstract
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


