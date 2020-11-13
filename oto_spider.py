# -*- coding: utf-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request

class otodom(scrapy.Spider):
    name = 'oto'
    custom_settings = {'FEEDS':{'results1.csv':{'format':'csv'}}}
    start_urls = ['https://www.otodom.pl/wynajem/dom/']
    headers = {
                'user-agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    }

    def parse(self, response):
        self.logger.debug('callback "parse": got response %r' % response)
        cards = response.xpath('//div[@class="offer-item-details"]')
        for card in cards:
            price = card.xpath('.//*[@class="offer-item-price"]/text()').get().replace('\n','').replace('/mc','').strip()
            title = card.xpath('.//*[@class="offer-item-title"]/text()').get()
            rooms = card.xpath('.//*[@class="offer-item-rooms hidden-xs"]/text()').get().split()[0]
            link = card.css('h3 a::attr(href)').get()

            request = Request(link, callback=self.parse_details, meta={'price':price,'title':title,'rooms':rooms,'link':link})
            yield request

        next_url = response.xpath('//li[@class="pager-next"]/a/@href').get()
        if next_url:
            # go to next page until no more pages
            yield response.follow(next_url, callback=self.parse)
    
    def parse_details(self,response):
        opis = response.css('p::text').getall()
        # get sqm and other shizz from details page
        price = response.meta['price']
        title = response.meta['title']
        rooms = response.meta['rooms']
        link = response.meta['link']
        #
        yield {'price':price,'title':title,'rooms':rooms,'link':link, 'opis':opis}
            

# main driver
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(otodom)
    process.start()
