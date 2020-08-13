import scrapy

class NewsItem(scrapy.Item):
    """Items extracted from the news
    """
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    volanta = scrapy.Field()
    body = scrapy.Field()

