import scrapy
from ..items import AuthorItem


class AboutAuthorSpider(scrapy.Spider):
    name = 'about_author'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'homework_spyder.pipelines.AboutAuthorPipeline': 100
        }
    }

    def parse(self, response):
        doc = AuthorItem()
        page = response.xpath("/html//div[@class='quote']")
        if page:
            for quote in page:
                url = 'http://quotes.toscrape.com' + quote.xpath('span/a/@href').get()
                yield scrapy.Request(url=url)

            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                yield scrapy.Request(url=self.start_urls[0] + next_link)
        else:
            doc['author'] = response.xpath("/html/body/div/div[2]/h3/text()").get()
            doc['birthday'] = response.xpath("/html/body/div/div[2]/p[1]/span[1]/text()").get()
            doc['description'] = response.xpath("/html/body/div/div[2]/div/text()").get()
            yield doc

