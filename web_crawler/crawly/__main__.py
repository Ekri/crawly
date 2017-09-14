from websiteretriever import WebsiteRetriever
from websiteretriever import EndlessWebsiteRetriever
from cache.urls_cache import UrlCache
from crawlies.Crawly import WordsCrawly
import db_uris

retriv = WebsiteRetriever(UrlCache(db_uris.WRITE_URI), max_pages=10)
retriv.add_crawlies(WordsCrawly(UrlCache("db/matches.db"), "wiara"))
retriv.retrieve("http://biblia.deon.pl/")
