import requests
import bs4

from common import config

class NewsPage:

    def __init__(self, news_site_uid, url):
        self._config = config()[ 'news_sites'][news_site_uid]
        self._queries = self._config['queries'] #This variable contains the CSS Selectors of the file config.yaml
        self._html = None
        self._url = url
        self._visit(url)        

    def _select(self, query_string):
        """
        The argument query_string contains the CSS selector to search in the _html variable
        It uses BS4 library to search all the content with that selectors and return 
        a list with all the elements that match with the selectors
        """
        return self._html.select(query_string)

    def _visit(self, url):
        """
        
        """
        response = requests.get(url)  # This variable stores the complete web site, use response.text to watch the content in a string
        response.raise_for_status()

        self._html = bs4.BeautifulSoup(response.text, 'html.parser')


class HomePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    
    @property
    def article_links(self):
        link_list = []

        for link in self._select(self._queries['homepage_article_links']):
            if link.has_attr('href'):
                link_list.append(link)
                
        return set(link['href'] for link in link_list)                


class ArticlePage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def url(self):
        return self._url

    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        
        return result[0].text if len(result)  else ''

    @property
    def title(self):
        
        result = self._select(self._queries['article_title'])

        return result[0].text if len(result) else ''
