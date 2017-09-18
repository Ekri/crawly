import urllib2


class Crawly(object):
    def crawl(self, url):
        self.url = url


class CachedCrawly(Crawly):
    def __init__(self, cache):
        self.cache = cache

    def cache_url(self, url):
        self.cache.set(url)


class WebsiteCrawly(Crawly):
    def get_website(self, url):
        return urllib2.urlopen(url).read()


class WordsCrawly(CachedCrawly, WebsiteCrawly):
    def __init__(self, word_cache, seek_words):
        super(WordsCrawly, self).__init__(word_cache)
        self.seek_words = seek_words

    def crawl(self, url):
        super(WordsCrawly, self).crawl(url)
        try:
            website = self.get_website(url)
            if self.seek_words in website:
                print "Word is in website: ", url
                self.cache_url(url)
            else:
                print "Doesn`t find word in: ", url
        except Exception as exc:
            print exc


class MultipleWordsCrawly(CachedCrawly, WebsiteCrawly):
    def __init__(self, word_cache, *args):
        super(MultipleWordsCrawly, self).__init__(word_cache)
        self.words = args

    def crawl(self, url):
        super(MultipleWordsCrawly, self).crawl(url)
        try:
            website = self.get_website(url)
            for word in self.words:
                if word in website:
                    print "Word: ", word, " is in website: ", url
                    self.cache_url(url)
                print "Doesn`t find word", word, "in: ", url
        except Exception as exc:
            print exc
