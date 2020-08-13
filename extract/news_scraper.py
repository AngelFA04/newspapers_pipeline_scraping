import scrapy
from items import NewsItem
import yaml
import os
from common import config_dict

DEPTH_LIMIT = 6
_DEBUGGING = False
import pdb


class NewsScraper(scrapy.Spider):
    name = 'scraper'

    custom_settings = {
            'FEED_EXPORT_ENCODING':'utf-8',
            'DEPTH_LIMIT':DEPTH_LIMIT,
            'FEED_FORMAT':'json', 
    }
    
    def __init__(self, website, *args, **kwargs, ):
        super(NewsScraper, self).__init__(website, *args, **kwargs)
        self.current_newspaper = config_dict()['news_sites'][website]
        self.newspaper_name = website
        self.start_urls = self.current_newspaper['url']
        self.queries = self.current_newspaper['queries']


    def parse(self, response):

        news = response.css(self.queries['homepage_article_links']).getall()

        for new in news:
            yield response.follow(new, callback=self.parse_new)

        button_next = response.css(self.queries['next_button_link']).get()

        if button_next:
            yield response.follow(button_next, callback=self.parse)
         

    def parse_new(self, response):
        """Extract the data from each new.

        Args:
            response ([http.response]): [Http response from the news article]

        Returns:
            newspage[item object]: [A dictionary with the data from the news]
        """
        
        body = response.css(self.queries['article_body']).getall() #s_nota.find("div", attrs={"class":"article-text"}).text
        
        if not body:
            return None
        elif body:
            if ''.join(body).strip() == '':
                return None

        title = response.css(self.queries['article_title']).get(default='')
        date = response.css(self.queries['date']).get()
        body = ''.join(body)

        try:
            volanta = response.css(self.queries['volanta']).get() #s_nota.find("div", attrs={"class":"article-prefix"}).text
        except:
            volanta = ''
        
        if _DEBUGGING:
            pdb.set_trace()

        newspage = NewsItem()

        newspage['url'] = response.url
        newspage['title'] = title
        newspage['date'] = date
    #    newspage['volanta'] = volanta
        newspage['body'] = body

        yield newspage


if __name__ == "__main__":
    with open('config.yaml', mode='r') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)