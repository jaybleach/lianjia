# -*- coding: utf-8 -*-
from scrapy import Request, Spider
import json
from lianjia.items import LianjiaItem
import redis

class HouseSpider(Spider):
    name = 'house'
    allowed_domains = ['bj.lianjia.com']
    max_page = 2

    def start_requests(self):
        base_url = 'https://bj.lianjia.com/ershoufang/dongcheng/pg1/'
        # pagelist = requests.get('https://bj.lianjia.com/ershoufang/dongcheng/pg1/')
        # page = pagelist.xpath('.//div[contains(@class, "page-box house-lst-page-box")]/@page-data').extract()
        # print(page)
        yield Request(base_url, callback=self.page)

    def page(self, response):
        page = response.xpath('.//div[contains(@class, "page-box house-lst-page-box")]/@page-data').extract()
        pages = json.loads(page[0])
        self.max_page = pages['totalPage']
        for i in range(self.max_page + 1):
            url = 'https://bj.lianjia.com/ershoufang/dongcheng/pg' + str(i)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        r = redis.Redis(host='127.0.0.1', port=6379, db=1)

        details = response.xpath('.//li[contains(@class, "clear LOGCLICKDATA")]')

        for detail in details:
            item = LianjiaItem()
            item['title'] = detail.xpath('.//div[@class="title"]/a//text()').extract_first()

            temp = ''
            list = detail.xpath('.//div[@class="houseInfo"]//text()').extract()
            for i in range(11): temp = temp + list[i]
            item['houseInfo'] = temp

            temp = ''
            list = detail.xpath('.//div[@class="positionInfo"]//text()').extract()
            for i in range(5): temp = temp + list[i]
            item['positionInfo'] = temp

            temp = ''
            list = detail.xpath('.//div[@class="followInfo"]//text()').extract()
            for i in range(3): temp = temp + list[i]
            item['followInfo'] = temp

            temp = ''
            list = detail.xpath('.//div[@class="tag"]/span//text()').extract()
            for i in range(2): temp = temp + list[i] + " "
            item['tag'] = temp

            temp = ''
            list = detail.xpath('.//div[@class="totalPrice"]//text()').extract()
            for i in range(2): temp = temp + list[i] + " "
            item['total'] = temp

            item['unit'] = detail.xpath('.//div[@class="unitPrice"]/span//text()').extract_first()
            item['detail_url'] = detail.xpath('.//div[@class="title"]/a/@href').extract_first()

            idkey = 'name' + json.dumps(item['title'])
            r.hmget(idkey, json.dumps(item.collection))
            r.hset(idkey, 'title', json.dumps(item['title']))
            r.hset(idkey, 'houseInfo', json.dumps(item['houseInfo']))
            r.hset(idkey, 'positionInfo', json.dumps(item['positionInfo']))
            r.hset(idkey, 'followInfo', json.dumps(item['followInfo']))
            r.hset(idkey, 'tag', json.dumps(item['tag']))
            r.hset(idkey, 'total', json.dumps(item['total']))
            r.hset(idkey, 'unit', json.dumps(item['unit']))
            r.hset(idkey, 'detail_url', json.dumps(item['detail_url']))
            yield item

        # r.set(idkey, json.dumps(item.collection))
        print(item.collection)



