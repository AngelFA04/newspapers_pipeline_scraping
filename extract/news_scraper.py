import scrapy
from items import NewsItem
import yaml
import os
from common import config_dict


class NewsScraper(scrapy.Spider):
    name = 'scraper'

    custom_settings = {
            'FEED_EXPORT_ENCODING':'utf-8',
            'DEPTH_LIMIT':5,
            'FEED_FORMAT':'json', 
    }
    
    def __init__(self, website, *args, **kwargs, ):
        super(NewsScraper, self).__init__(website, *args, **kwargs)
        self.current_newspaper = config_dict()['news_sites'][website]
        self.newspaper_name = website
        self.start_urls = self.current_newspaper['url']
        self.queries = self.current_newspaper['queries']
        #allowed_domains = ['www.pagina12.com.ar']


    
    ###### Abstraction here

    def parse(self, response):
        #Nota promocionada
    ###### Abstraction here

        #nota_promocionada = response.xpath('//div[@class="featured-article__container"]/h2/a/@href').get()
        
        #import pdb; pdb.set_trace()

        # if nota_promocionada is not None:
        #     yield response.follow(nota_promocionada, callback=self.parse_nota)

        #Listado de notas
    ###### Abstraction here
        notas = response.css(self.queries['homepage_article_links']).getall()

        for nota in notas:
            yield response.follow(nota, callback=self.parse_nota)

    ###### Abstraction here
        button_next = response.css(self.queries['next_button_link']).get()

        if button_next:
            yield response.follow(button_next, callback=self.parse)
         

    def parse_nota(self, response):
        """
     FULL OF ABSTRACTION 
        """
        
        cuerpo = response.css(self.queries['article_body']).getall() #s_nota.find("div", attrs={"class":"article-text"}).text
        
        if not cuerpo or cuerpo == '':
            return None

        titulo = response.css(self.queries['article_title']).get()
        fecha = response.css(self.queries['date']).get()
        cuerpo = ''.join(cuerpo)
        #import pdb; pdb.set_trace()
        try:
            volanta = response.css(self.queries['volanta']).get() #s_nota.find("div", attrs={"class":"article-prefix"}).text
        except:
            volanta = None

        newspage = NewsItem()

        newspage['url'] = response.url
        newspage['title'] = titulo
        newspage['date'] = fecha
    #    newspage['volanta'] = volanta
        newspage['body'] = cuerpo

        yield newspage


if __name__ == "__main__":
    pass
    with open('config.yaml', mode='r') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)