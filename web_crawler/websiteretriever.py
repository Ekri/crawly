import httplib2
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from datetime import datetime

HTML_PARSER = "html.parser"


class WebsiteRetriever(object):
    def __init__(self, cache=None, max_pages=10):
        self.cache = cache
        if self.cache is None:
            raise ValueError("Cache cannot be None.")
        self.maxPages = max_pages
        self.consumers = []
        self.urls = []
        self.visited = 0

    def add_crawlies(self, *args):
        for consumer in args:
            self.consumers.append(consumer)

    def retrieve(self, url):
        self.urls.append(url)

        while self.loop_condition():
            http = httplib2.Http()
            current_url = self.urls[self.visited]

            try:
                print "Fetching: " + current_url
                status, response = http.request(current_url)
                self.parse_html(response)
                for crawly in self.consumers:
                    crawly.crawl(current_url)

            except httplib2.HttpLib2Error as err:
                print "Fetching error: ", err

            self.visited += 1

    def parse_html(self, response):
        for url in BeautifulSoup(response, HTML_PARSER, parse_only=SoupStrainer('a')):
            if url.has_attr('href'):
                url_retrieved = url['href']
                print "retrieving...", url_retrieved
                self.cache_url(url_retrieved)
                self.urls += url_retrieved

    def cache_url(self, url):
        self.cache.set(url)

    def loop_condition(self):
        return self.visited < self.maxPages


class TimingWebsiteRetriever(WebsiteRetriever):
    def __init__(self, cache=None, t_to_run=datetime.now()):
        super(TimingWebsiteRetriever, self).__init__(cache, 0)
        self.t_to_run = t_to_run
        if self.t_to_run is None or self.t_to_run < datetime.now():
            raise ValueError("Time to run cannot be None or  lower then now")

    def loop_condition(self):
        return datetime.now() < self.t_to_run
