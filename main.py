# coding=utf-8
import sys

from classifier import Classifier
from spider import Spider

def train(cl, blog):
    s = Spider(cl.train)
    s.parse_blog(blog)


def test(cl):
    from pprint import pprint
    pprint(cl.check(u'''Але сесії завтра прийде кінець, тому почну рухатись.
    В університет мені їхати досить довго – від Ⓜ “червоний хутір” аж до Ⓜ “Виставковий центр”,
    але завдяки Kindle мені на кінцевій навіть виходити не хочеться – хочеться читати далі.
    '''))

def main(mode='test'):
    cl = Classifier()
    cl.create_db('base.db')

    if mode == 'test':
        test(cl)
    else:
        train(cl, 'http://bunyk.wordpress.com')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'test')
