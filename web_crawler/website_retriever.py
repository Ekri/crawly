import httplib2
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from datetime import datetime
from helpers.urls_nicer import URLRepairer

HTML_PARSER = "html.parser"


class WebsiteRetriever(object):
    def __init__(self, cache=None, max_pages=10):
        self.cache = cache
        if self.cache is None:
            raise ValueError("Cache cannot be None.")
        self.maxPages = max_pages
        self.consumers = []
        self.urls = []
        self.visitedPages = []
        self.visited = 0

    def add_crawlies(self, *args):
        for consumer in args:
            self.consumers.append(consumer)

    def retrieve(self, url):
        self.urls.append(url)
        repairer = URLRepairer()

        for url in self.urls:
            if not self.loop_condition():
                break

            http = httplib2.Http()

            current_url = repairer.repair_url_with_domain(url)

            try:
                print "Fetching: " + current_url
                status, response = http.request(current_url)
                repairer.get_domain(current_url)
                self.parse_html(response)
                for crawly in self.consumers:
                    crawly.crawl(current_url)

            except httplib2.HttpLib2Error as err:
                print "Fetching error: ", err

            self.visitedPages.append(current_url)
            self.remove_item(current_url)
            self.visited += 1

    def parse_html(self, html):
        for tag in BeautifulSoup(html, HTML_PARSER, parse_only=SoupStrainer('a', href=True)):
            if tag is not None:
                url_retrieved = tag['href']
                print "retrieving...", url_retrieved
                self.cache_url(url_retrieved)
                if url_retrieved not in self.visitedPages:
                    self.urls.append(url_retrieved)

    def cache_url(self, url):
        self.cache.set(url)

    def loop_condition(self):
        return self.visited < self.maxPages

    def remove_item(self, item):
        try:
            self.urls.remove(item)
        except ValueError:
            pass


class TimingWebsiteRetriever(WebsiteRetriever):
    def __init__(self, cache=None, t_to_run=datetime.now()):
        super(TimingWebsiteRetriever, self).__init__(cache, 0)
        self.t_to_run = t_to_run
        if self.t_to_run is None or self.t_to_run < datetime.now():
            raise ValueError("Time to run cannot be None or lower then now")

    def loop_condition(self):
        return datetime.now() < self.t_to_run


class EndlessWebsiteRetriever(WebsiteRetriever):
    def __init__(self, cache=None):
        super(EndlessWebsiteRetriever, self).__init__(cache, 0)

    def loop_condition(self):
        return self.urls
