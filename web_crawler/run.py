from urls_cache import UrlCache
from db_uris import READ_URI

reader = UrlCache(READ_URI)
list1 = reader.get_all()
for url in list1:
    print url
