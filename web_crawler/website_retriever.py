import httplib2
from bs4 import BeautifulSoup
from bs4 import SoupStrainer


class website_retriever(object):
    def __init__(self, cache=None, maxPages=10):
        self.cache = cache
        self.maxPages = maxPages

    def retrieve(self, url):
        self.links = []
        self.links.append(url)
        numberVisited = 0

        # for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
        #     if link.has_attr('href'):
        #         self.links.append(link['href'])
        #         print link['href']
        while numberVisited < self.maxPages:
            htttp = httplib2.Http()
            currentUrl = self.links[numberVisited]
            numberVisited = numberVisited + 1
            status, response = htttp.request(currentUrl)
            self.parseHtml(response)

    def parseHtml(self, response):
        for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                self.links.append(link['href'])
                print link['href']


retriv = website_retriever()
retriv.retrieve("http://www.interia.pl")
