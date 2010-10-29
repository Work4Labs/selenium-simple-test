import time

from selenium import FIREFOX
from selenium.remote import connect
from selenium.common.exceptions import (
    NoSuchElementException, NoSuchAttributeException
)


__all__ = [
    'start', 'stop', 'title_is', 'goto', 'waitfor', 'fails', 'url_is',
    'is_radio', 'set_base_url', 'reset_base_url', 'radio_value_is'
]

browser = None

BASE_URL = 'http://localhost:8000/'
__DEFAULT_BASE_URL__ = BASE_URL
VERBOSE = True


def _raise(msg):
    _print(msg)
    raise AssertionError(msg)


def set_base_url(url):
    global BASE_URL
    BASE_URL = url


def reset_base_url():
    global BASE_URL
    BASE_URL = __DEFAULT_BASE_URL__


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
        url = BASE_URL + url
    return url


def goto(url=''):
    url = _fix_url(url)
    _print('Going to... %s' % url)
    browser.get(url)


def title_is(title):
    real_title = browser.get_title()
    msg = 'Title is: %r. Should be: %r' % (real_title, title)
    if not real_title == title:
        _raise(msg)


def url_is(url):
    url = _fix_url(url)
    real_url = browser.get_current_url()
    msg = 'Url is: %r\nShould be: %r' % (real_url, url)
    if not url == real_url:
        _raise(msg)

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
            _raise(error)
        time.sleep(poll)


def fails(action, *args, **kwargs):
    try:
        action(*args, **kwargs)
    except AssertionError:
        return
    msg = 'Action %r did not fail' % action.__name__
    _raise(msg)


def _get_elem(the_id):
    try:
        return browser.find_element_by_id(the_id)
    except NoSuchElementException:
        msg = 'Element %r does not exist' % the_id
        _raise(msg)


def _elem_is_type(elem, name, elem_type):
    msg = 'Element %r is not a %r' % (name, elem_type)
    try:
        result = elem.get_attribute('type')
    except NoSuchAttributeException:
        _raise(msg)
    if not result == elem_type:
        _raise(msg)


def is_radio(the_id):
    elem = _get_elem(the_id)
    _elem_is_type(elem, the_id, 'radio')
    return elem


def radio_value_is(the_id, value):
    elem = is_radio(the_id)
    selected = elem.is_selected()
    msg = 'Radio %r should be set to: %s.' % (the_id, value)
    if value != selected:
        _raise(msg)

