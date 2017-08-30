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

        # for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
        #     if link.has_attr('href'):
        #         self.links.append(link['href'])
        #         print link['href']
        while number_visited < self.maxPages:
            http = httplib2.Http()
            current_url = self.links[number_visited]
            number_visited = number_visited + 1
            try:
                status, response = http.request(current_url)
                self.parse_html(response)
                self.seek_word(current_url, response, phrase)
            except httplib2.HttpLib2Error as err:
                print err

    def parse_html(self, response):
        for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                linkRetrieved = link['href']
                print "retrieving...", linkRetrieved
                self.cache.set(linkRetrieved)
                self.links.append(linkRetrieved)

    def seek_word(self, url, htlm, word):
        # soup = BeautifulSoup(htlm, "html.parser")
        # result = soup.findAll(text=word)
        # print "result: ", result
        website = urllib2.urlopen(url).read()
        if word in website:
            print "Word is in website: ", url
            self.wordCache.set(url)


retriv = website_retriever(RetrieverCache("db/retrieved.db"), RetrieverCache("word.db"), max_pages=1)
retriv.retrieve("https://www.reuters.com/article/us-usa-afghanistan-minerals-idUSKCN1B102L", "reuters")
