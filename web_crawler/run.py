import re
from inner_crawler import Crawler
from SimpleCache import CrawlerCache


if __name__ == "__main__":
    crawler = Crawler(CrawlerCache("crawler.db"))
    root_re = re.compile('^/$').match
    crawler.crawl('http://techcrunch.com/', no_cache=root_re)
