from urlparse import urljoin


class URLRepairer(object):
    def __init__(self, *args, **kwargs):
        self._domain = kwargs.pop('domain', None)

    def get_domain(self, url):
        self._domain = urljoin(url, '/')
        print "Domain: ", self._domain

    def repair_url_with_domain(self, url):
        if url.startswith("http://") or url.startswith("https://"):
            return url
        else:
            if self._domain is None:
                raise ValueError("Domain cannot be None")
            return self._domain + url
