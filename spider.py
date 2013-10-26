import requests
import requests_cache

from util import data_file
from parsers import get_page_content_cc, iter_pages

requests_cache.install_cache(data_file('cache'))

def wget(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text

class Spider(object):
    def __init__(self, train_f):
        self.train_f = train_f

    def parse_blog(self, url):
        if not url.endswith('/'): # url must end with slash
            url = url + '/'

        sitemap = wget(url + 'sitemap.xml')

        for page in iter_pages(sitemap):
            if is_article(page):
                self.parse_page(page)

    def parse_page(self, page):
        text = wget(page)
        content, cc = get_page_content_cc(text)
        self.train_f(content, cc)

def is_article(url):
    ''' When count of slashes in url is less than 7 - this is not article '''
    return sum(1 for c in url if c == '/') >= 7

