import httplib2
import urllib2
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from RetrieverCache import RetrieverCache


class website_retriever(object):
    def __init__(self, cache=None, wordCache=None, maxPages=10):
        self.cache = cache
        self.maxPages = maxPages
        self.wordCache = wordCache

    def retrieve(self, url, phrase=None):
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
            try:
                status, response = htttp.request(currentUrl)
                self.parseHtml(response)
                self.seekWord(currentUrl, response, phrase)
            except httplib2.HttpLib2Error as err:
                print err

    def parseHtml(self, response):
        for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                linkRetrieved = link['href']
                print "retrieving...", linkRetrieved
                self.cache.set(linkRetrieved)
                self.links.append(linkRetrieved)

    def seekWord(self, url, htlm, word):
        # soup = BeautifulSoup(htlm, "html.parser")
        # result = soup.findAll(text=word)
        # print "result: ", result
        website = urllib2.urlopen(url).read()
        if word in website:
            self.wordCache.set(url)


retriv = website_retriever(RetrieverCache("retrieved.db"), RetrieverCache("word.db"), maxPages=1)
retriv.retrieve("https://www.reuters.com/article/us-usa-afghanistan-minerals-idUSKCN1B102L", "dupa")
