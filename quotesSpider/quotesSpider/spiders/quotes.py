# -*- coding: utf-8 -*-
import scrapy

from quotesSpider.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        '''
        解析网页数据
        :param response: 是requests请求后的结果
        :return: 用yield来返回字典型的数据
        '''

        # 从response中得到一个类名为quote的数据
        quotes = response.css('.quote')

        for quote in quotes:
            # 调用QuotesItem()类来存储数据
            item = QuotesItem()
            # ::这是scrapy特有的一个功能像当于一个pyquery一样的选择器
            text = quote.css('.text::text').extract_first()
            # ::text是指取出其中的文本数据,.extract_first意思是找第一个
            author = quote.css('.author::text').extract_first()
            # 因为tags可以有多个所以不能用前两句的方式了，只能用这种并extract()指取多个
            tags = quote.css('.tags .tag::text').extract()

            # 然后再把数据存储到QuotesItem()中以字典方式存储
            item['text'] = text
            item['author'] = author
            item['tags'] = tags

            # 调用yield方法来回传数据
            yield item

        # 得到下一页的url连接
        next = response.css('.pager .next a::attr(href)').extract_first()
        # 因为此时拿到的数据是一个相对的url:/page/2/，所以需要加上前面的url连接在一起，组成一个绝对的url
        url = response.urljoin(next)
        # 首先生成一个requests对象，第一个参数是url，第二个参数callback回调函数和pyspider里的一样，把得到的新的url也就是下一页的url再次的递归的调用自己
        yield scrapy.Request(url=url, callback=self.parse)
