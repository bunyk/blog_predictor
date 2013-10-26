import re
from lxml import etree

from BeautifulSoup import BeautifulSoup
import soupselect

def iter_pages(sitemap):
    ''' Convert sitemap text to iterator throught urls '''

    tree = etree.fromstring(sitemap.encode('utf-8'))

    # XPath selector finds all "loc" elements in sitemap namespace
    return (
        element.text for element in
        tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
    )

def clean_html(html):
    """ Remove HTML markup from the given string."""
    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(ur"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments.
    # This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(ur"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(ur"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(ur"&nbsp;", " ", cleaned)
    cleaned = re.sub(ur"\s+", " ", cleaned)
   
    return cleaned.strip()


TOKENIZE_REGEX = re.compile(ur'([\w`-]+|[^\w\s]|\s+)', re.U)
 
def tokenize(text):
    return (s.groups()[0] for s in TOKENIZE_REGEX.finditer(text))

THEMES_SELECTORS = (
    ('journalist', 'div.main', 'h3.reply'),
    ('liquorice', 'div.entry', 'p.comments-num a'),
)

def select(soup, selector):
    nodes = soupselect.select(soup, selector)
    return unicode(nodes[0]) if nodes else ''

def get_comment_count(html_node):
    text = clean_html(html_node).strip().lower()
    if not text:
        return 0
    if 'one' in text:
        return 1
    numbers = re.findall('\d+', text)
    if numbers:
        return int(numbers[0])
    else:
        raise ValueError('Unknown comment count: %r' % text)

def get_page_content_cc(html):
    parsed = BeautifulSoup(html)
    for theme, content_query, cc_query in THEMES_SELECTORS:
        if ('theme.wordpress.com/themes/%s/' % theme) in html:
            main = select(parsed, content_query)
            cc = select(parsed, cc_query)
            return clean_html(main), get_comment_count(cc)

    raise ValueError('Unknown theme')

