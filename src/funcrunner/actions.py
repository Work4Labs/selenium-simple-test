import time

from selenium import FIREFOX
from selenium.remote import connect


__all__ = [
    'start', 'stop', 'title_is', 'goto', 'waitfor'
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
