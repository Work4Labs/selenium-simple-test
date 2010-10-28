from selenium import FIREFOX
from selenium.remote import connect


__all__ = [
    'start', 'stop', 'title_is', 'goto'
]

browser = None

DEFAULT_URL = 'http://localhost:8000/'
VERBOSE = True

def _print(text):
    if VERBOSE:
        print text


def start():
    global browser
    _print('Starting browser')
    browser = connect(FIREFOX)


def stop():
    global browser
    _print('Stopping browser')
    browser.close()
    browser = None


def goto(url=''):
    if url.startswith('/'):
        url = url[1:]
    if not url.startswith('http:'):
        url = DEFAULT_URL + url

    _print('Going to... %s' % url)
    browser.get(url)


def title_is(title):
    real_title = browser.get_title()
    msg = 'Title is: %r. Should be: %r' % (real_title, title)
    if not real_title == title:
        print msg

    assert title == real_title, msg
