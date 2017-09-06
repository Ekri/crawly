import httplib2
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from crawlies.Crawly import WordsCrawly
from urls_cache import UrlCache
import db_uris


class website_retriever(object):
    def __init__(self, cache=None, max_pages=10):
        self.cache = cache
        self.maxPages = max_pages
        self.consumers = []
        self.links = []

    def add_crawlies(self, *args):
        for consumer in args:
            self.consumers.append(consumer)

    def retrieve(self, url):
        self.links.append(url)
        number_visited = 0

        while number_visited < self.maxPages:
            http = httplib2.Http()
            current_url = self.links[number_visited]

            try:
                print "Fetching: " + current_url
                status, response = http.request(current_url)
                self.parse_html(response)
                for crawly in self.consumers:
                    crawly.crawl(current_url)

            except httplib2.HttpLib2Error as err:
                print "Fetching error: ", err

            number_visited = number_visited + 1

    def parse_html(self, response):
        for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                link_retrieved = link['href']
                print "retrieving...", link_retrieved
                self.cache.set(link_retrieved)
                self.links.append(link_retrieved)


retriv = website_retriever(UrlCache(db_uris.READ_URI),
                           max_pages=100)
retriv.add_crawlies(WordsCrawly(UrlCache("db/matches.db"), "wiara"))
retriv.retrieve("http://biblia.deon.pl/")
