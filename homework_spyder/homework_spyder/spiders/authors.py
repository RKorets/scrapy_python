import scrapy
from ..items import AllDataItem


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'homework_spyder.pipelines.AllDataPipeline': 100
        }
    }

    def parse(self, response):
        doc = AllDataItem()
        for quote in response.xpath("/html//div[@class='quote']"):
            doc['url'] = 'http://quotes.toscrape.com' + quote.xpath('span/a/@href').get()
            doc['keywords'] = quote.xpath("div[@class='tags']/a/text()").extract()
            doc['author'] = quote.xpath("span/small/text()").extract()
            doc['quote'] = quote.xpath("span[@class='text']/text()").get()
            yield doc
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
