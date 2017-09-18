from cache.urls_cache import UrlCache
import db_uris

reader = UrlCache(db_uris.READ_URI)
list1 = reader.get_all()
for url in list1:
    print url
