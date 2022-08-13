import scrapy


class AllDataItem(scrapy.Item):
    url = scrapy.Field()
    keywords = scrapy.Field()
    author = scrapy.Field()
    quote = scrapy.Field()


class AuthorItem(scrapy.Item):
    author = scrapy.Field()
    birthday = scrapy.Field()
    description = scrapy.Field()

