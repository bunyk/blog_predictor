# coding=utf-8
from __future__ import unicode_literals

import unittest


class TestPersistence(unittest.TestCase):
    def setUp(self):
        from model import Persistence
        self.persistence = Persistence()
        self.persistence.create_db(':memory:')

    def test_empty_feature_count(self):
        self.assertEquals(self.persistence.fcount('viagra', 'spam'), 0)

    def test_increment_feature_count(self):
        self.persistence.incf('viagra', 'spam')
        self.assertEquals(self.persistence.fcount('viagra', 'spam'), 1)

    def test_empty_cat_count(self):
        self.assertEquals(self.persistence.catcount('spam'), 0)

    def test_increment_cat_count(self):
        self.persistence.incc('spam')
        self.assertEquals(self.persistence.catcount('spam'), 1)

class TestParsers(unittest.TestCase):
    def test_sitemap_parsing(self):
        from parsers import iter_pages
        sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
        <!-- generator="wordpress.com" -->
        <urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
          <url>
            <loc>https://vrubli.wordpress.com/2013/08/31/na_mezhi_mizh_proshchanniam_i_zustricchiu/</loc>
            <mobile:mobile/>
            <lastmod>2013-08-30T22:53:52+00:00</lastmod>
            <changefreq>monthly</changefreq>
          </url>
          <url>
            <loc>https://vrubli.wordpress.com/2013/08/30/vulytsya_do_yakoi_ne_distatys/</loc>
            <mobile:mobile/>
            <image:image>
              <image:loc>http://vrubli.files.wordpress.com/2013/08/149.jpg</image:loc>
              <image:title>Колії</image:title>
            </image:image>
            <lastmod>2013-08-30T21:29:34+00:00</lastmod>
            <changefreq>monthly</changefreq>
          </url>
        </urlset>
        '''
        self.assertEquals(list(iter_pages(sitemap)), [
            'https://vrubli.wordpress.com/2013/08/31/na_mezhi_mizh_proshchanniam_i_zustricchiu/',
            'https://vrubli.wordpress.com/2013/08/30/vulytsya_do_yakoi_ne_distatys/',
        ])

    def test_get_page_content_cc(self):
        from spider import wget
        from parsers import get_page_content_cc

        self.assertEquals(get_page_content_cc(wget('http://bunyk.wordpress.com/2013/10/26/mind-fog/'))[1], 2)
        self.assertEquals(get_page_content_cc(wget('http://bunyk.wordpress.com/2013/10/13/sport-movie/'))[1], 0)
        self.assertEquals(get_page_content_cc(wget('http://bunyk.wordpress.com/2013/10/14/im-nebel/'))[1], 1)

        res = get_page_content_cc(wget('http://vrubli.wordpress.com/2013/03/26/konkretnym_ne_konkretyzujchy/'))
        self.assertEquals(res[1], 6)

    def test_tokenizer(self):
        from parsers import tokenize
        self.assertEquals(
            list(tokenize('буттям «кинутої ')), 
            ['буттям', 'кинутої'],
        )


class TestSpider(unittest.TestCase):
    def test_wget(self):
        ''' Request to test service, returns correct params '''
        from spider import wget
        self.assertIn('test', wget('http://httpbin.org/get?q=test'))

    def test_grabbing(self):
        from spider import Spider
        def train(content, cc):
            raise StopIteration
        s = Spider(train)

        self.assertRaises(StopIteration, s.parse_blog, 'http://bunyk.wordpress.com/')

class TestClassifier(unittest.TestCase):
    def setUp(self):
        from classifier import Classifier
        self.cl = Classifier()
        self.cl.create_db(':memory:')

    def test_fprob(self):
        for x in range(9):
            self.cl.train('viagra', 'spam')
        self.cl.train('penis', 'spam')
        self.assertEquals(self.cl.fprob('viagra', 'spam'), 0.9)

    def test_weighted_prob_unknown(self):
        self.assertEquals(0.5,
            self.cl.weightedprob('viagra', 'spam')
        )

    def test_weighted_prob_biased(self):
        self.cl.train('viagra', 'spam')
        self.assertEquals(0.75,
            self.cl.weightedprob('viagra', 'spam')
        )

    def test_train_adds_category(self):
        self.cl.train('1 2', 1)
        self.assertEquals(list(self.cl.categories()), [1])

    def test_train(self):
        self.cl.train('1 2', 1)
        self.cl.train('2 3', 1)
        self.cl.train('3 4', 2)

        self.assertEquals(list(self.cl.categories()), [1, 2])

    def test_check_plain(self):
        tmp_prob = self.cl.weightedprob
        self.cl.weightedprob = self.cl.fprob

        for i in range(9):
            self.cl.train('penis', 'spam')
        self.cl.train('penis', 'ok')

        self.assertEquals(self.cl.check('penis')[0], ('spam', 0.9))

        self.cl.weightedprob = tmp_prob

if __name__ == '__main__':
    unittest.main()


