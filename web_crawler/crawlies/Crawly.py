import urllib2


class Crawly(object):
    def __init__(self):
        pass

    def crawl(self, url):
        self.url = url


class WordsCrawly(Crawly):
    def __init__(self, word_cache, seek_words):
        self.word_cache = word_cache
        self.seek_words = seek_words

    def crawl(self, url):
        super(WordsCrawly, self).crawl(url)
        try:
            website = urllib2.urlopen(url).read()
            if self.seek_words in website:
                print "Word is in website: ", url
                self.word_cache.set(url)

            else:
                print "Doesn`t find word in: " , url
        except Exception as exc:
            print exc
