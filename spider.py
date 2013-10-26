import requests

from util import data_file

http = httplib2.Http('.cache')

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

        # І зберігаємо кожну сторінку про яку пише sitemap:
        for page in iter_pages(sitemap):
            if self.is_article(page):
                self.parse_page(page, blogname)


class WordpressComSpider(Spider):

    @classmethod
    def is_article(cls, url):
        ''' Якщо кількість слешів в url менше семи - це не стаття '''
        return sum(1 for c in url if c == '/') >= 7
