# -*- coding: utf-8 -*-
import scrapy

from huaishiSpider.items import HuaishispiderItem


class ShiyuannewsSpider(scrapy.Spider):
    name = 'shiyuannews'
    allowed_domains = ['www.hnnu.edu.cn']
    start_urls = ['http://www.hnnu.edu.cn/199/list.htm']

    def parse(self, response):
        # 解析首页的url
        url_list = response.css('a[href*=page]::attr(href)').extract()
        date_list = response.css('.lb table tr td div::text').extract()
        # print(url_list)
        # print(date_list)
        # item = HuaishispiderItem()
        for url, date in zip(url_list, date_list):
            # item['urllist'] = list
            # yield item
            url = response.urljoin(url)
            # 首先生成一个requests对象，第一个参数是url，第二个参数callback回调函数和pyspider里的一样，把得到的新的url也就是下一页的url再次的递归的调用自己
            yield scrapy.Request(url=url, callback=lambda response, date=date: self.parse_one_page(response, date))

        # 得到下一页的url连接
        next = response.css('li.page_nav a.next::attr(href)').extract_first()
        # 因为此时拿到的数据是一个相对的url:/page/2/，所以需要加上前面的url连接在一起，组成一个绝对的url
        next_url = response.urljoin(next)
        # print(next_url)
        # 首先生成一个requests对象，第一个参数是url，第二个参数callback回调函数和pyspider里的一样，把得到的新的url也就是下一页的url再次的递归的调用自己
        yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_one_page(self, response, date):
        title = response.css('title::text').extract_first()
        source = response.css('.MsoNormal span::text').extract_first()
        content = response.css('#infocontent::text').extract_first()

        item = HuaishispiderItem()
        item['title'] = title
        item['source'] = source
        item['content'] = content
        item['date'] = date
        return item
