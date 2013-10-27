# coding=utf-8
import sys

from classifier import Classifier
from spider import Spider

def train(cl, blog):
    s = Spider(cl.train)
    s.parse_blog(blog)


def test(cl):
    inp = []
    for row in sys.stdin:
        inp.append(row.decode('utf-8'))

    res = cl.check(u'\n'.join(inp))
    for cat, prob in res:
        print cat, repr(prob)

def main(mode='test'):
    cl = Classifier()
    cl.create_db('bunyk.db')

    if mode == 'test':
        test(cl)
    else:
        train(cl, 'http://bunyk.wordpress.com')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'test')
