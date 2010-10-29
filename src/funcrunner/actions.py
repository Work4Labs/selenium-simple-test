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


def is_checkbox(chk_name):
    checkbox = browser.find_element_by_id(chk_name)
    elem_type = checkbox.get_attribute('type')
    msg = 'Element ID: %r. Should be element of type: checkbox'
    if elem_type != 'checkbox':
        print msg
    assert elem_type == 'checkbox', msg
    return checkbox
    

def checkbox_value_is(chk_name, val):
    checkbox = is_checkbox(chk_name)
    chk_value = checkbox.is_selected()
    msg = 'Checkbox: %r - Has Value: %r' % (chk_name, chk_value)
    assert chk_value == val, msg


def checkbox_toggle(chk_name):
    checkbox = is_checkbox(chk_name)
    chk_value = checkbox_value_is(chk_name)
    checkbox.toggle()
    chk_toggle = checkbox_value_is(chk_name)
    msg = 'Checkbox: %r - was not toggled, value remains: %r' % (chk_name, chk_value)
    if chk_value == chk_toggle:
        print msg
    assert chk_value != chk_toggle, msg


def checkbox_set(chk_name, new_value):
    checkbox = is_checkbox(chk_name)
    # There is no method to 'unset' a checkbox in the browser object
    current_value = checkbox_value_is(chk_name)
    if new_value != current_value:
        checkbox_toggle(chk_name)


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

