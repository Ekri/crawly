import httplib2
import urllib2
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from RetrieverCache import RetrieverCache


class website_retriever(object):
    def __init__(self, cache=None, word_cache=None, max_pages=10):
        self.cache = cache
        self.maxPages = max_pages
        self.wordCache = word_cache

    def retrieve(self, url, phrase=None):
        self.links = []
        self.links.append(url)
        number_visited = 0

        while number_visited < self.maxPages:
            http = httplib2.Http()
            current_url = self.links[number_visited]
            number_visited = number_visited + 1
            try:
                status, response = http.request(current_url)
                self.parse_html(response)
                self.seek_word(current_url, phrase)
            except httplib2.HttpLib2Error as err:
                print err

    def parse_html(self, response):
        for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                linkRetrieved = link['href']
                print "retrieving...", linkRetrieved
                self.cache.set(linkRetrieved)
                self.links.append(linkRetrieved)

    def seek_word(self, url, word):
        try:
            website = urllib2.urlopen(url).read()
            if word in website:
                print "Word is in website: ", url
                self.wordCache.set(url)

        except Exception as exc:
            print exc

retriv = website_retriever(RetrieverCache("dbs/faith/retrieved.db"), RetrieverCache("dbs/faith/matches.db"),
                           max_pages=100)
retriv.retrieve("http://biblia.deon.pl/", "wiara")

