import time

from selenium import FIREFOX
from selenium.remote import connect


__all__ = [
    'start', 'stop', 'title_is', 'goto', 'waitfor', 'fails', 'url_is'
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


def _fix_url(url):
    if url.startswith('/'):
        url = url[1:]
    if not url.startswith('http'):
        url = DEFAULT_URL + url
    return url


def goto(url=''):
    url = _fix_url(url)
    _print('Going to... %s' % url)
    browser.get(url)


def title_is(title):
    real_title = browser.get_title()
    msg = 'Title is: %r. Should be: %r' % (real_title, title)
    if not real_title == title:
        print msg

    assert title == real_title, msg


def url_is(url):
    url = _fix_url(url)
    real_url = browser.get_current_url()
    msg = 'Url is: %r\nShould be: %r' % (real_url, url)
    if not url == real_url:
        print msg
    assert url == real_url, msg

"""
# Example action using waitfor
def wait_for_title_to_change(title):
    def title_changed():
        return browser.get_title() == title

    waitfor(title_changed, 'title to change')
"""

def waitfor(condition, msg='', timeout=5, poll=0.1):
    start = time.time()
    max_time = time.time() + timeout
    while True:
        if condition():
            break
        if time.time() > max_time:
            error = 'Timed out waiting for: ' + msg
            _print(error)
            raise AssertionError(error)
        time.sleep(poll)


def fails(action, *args, **kwargs):
    try:
        action(*args, **kwargs)
    except AssertionError:
        return
    msg = 'Action %r did not fail' % action.__name__
    _print(msg)
    raise AssertionError(msg)
