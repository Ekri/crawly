from website_retriever import WebsiteRetriever
from cache.urls_cache import UrlCache
from crawlies.Crawly import WordsCrawly
import db_uris
import os

parentPath = os.path.dirname(os.getcwd())

writePath = db_uris.UrisHelper.get_path(parentPath, db_uris.FAITH_WRITE_READ_URI)
matchesPath = db_uris.UrisHelper.get_path(parentPath, db_uris.FAITH_WRITE_READ_MATCHES_URI)

retriv = WebsiteRetriever(UrlCache(writePath), max_pages=10)
retriv.add_crawlies(WordsCrawly(UrlCache(matchesPath), "wiara"))
retriv.retrieve("http://biblia.deon.pl/")
