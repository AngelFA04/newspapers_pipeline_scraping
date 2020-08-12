import scrapy

class NewsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    volanta = scrapy.Field()
    body = scrapy.Field()

