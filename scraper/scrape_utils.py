import requests
from scraper.newspaper_git.newspaper import Article, Config, Source
from waybackpy import Url
from time import sleep
from random import randint


def get_article(url):
    article=Article(url)
    article.download()
    article.parse()
    return article.text

class wayback_scraper:
    def __init__(self, url, agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'):
        self.agent=agent
        self.wayback_obj = Url(url, agent)
        #print(self.wayback_obj)
        self.wayback_url = None
    
    def set_date(self, y, m, d):
        self.wayback_url = str(self.wayback_obj.near(year=y, month=m, day=d))
        updated_url = self.wayback_url.split("/")
        #print(updated_url)
        updated_url[5] = "https:"
        self.wayback_url = "/".join(updated_url)
        #print(self.wayback_url)
        
    def get_articles(self, timeout=None):
        #Returns a list of newspaper articles
        
        if self.wayback_url == None:
            raise ValueError("Must set date with set_date function")
        
        config = Config()
        config.browser_user_agent = self.agent
        config.request_timeout = timeout
        config.memoize_articles = False
        config.language='en'
        config.number_threads = 20
        config.threat_timeout_seconds=2
        config.verbose=False
        wayback = Source(url=self.wayback_url, config=config)       
        wayback.build()
        
        return wayback.articles
    
    def search_by_title(self, keywords):
        
        articles=self.get_articles()
        ret_articles = []
        
        for article in articles:
            #print(article.url)
            if type(article.title) == str:
                if any(word in article.title for word in keywords):
                    if article not in ret_articles:
                        ret_articles.append(article)
    
        return ret_articles
    def search_by_text(self,keywords):
        articles=self.get_articles()
        ret_articles = []
        
        for article in articles:
            #print(article.url)
            try:
                article.download()
                article.parse()
            except:
                continue
            else:
                if type(article.title) == str:
                    if any(word in article.title for word in keywords):
                        if article not in ret_articles:
                            ret_articles.append(article)