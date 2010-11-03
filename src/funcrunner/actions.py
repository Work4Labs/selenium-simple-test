import time

from selenium import FIREFOX
from selenium.remote import connect
from selenium.common.exceptions import (
    NoSuchElementException, NoSuchAttributeException
)
from selenium.remote.webelement import WebElement


__all__ = [
    'start', 'stop', 'title_is', 'goto', 'waitfor', 'fails', 'url_is',
    'is_radio', 'set_base_url', 'reset_base_url', 'radio_value_is',
    'radio_select', 'text_is', 'is_checkbox', 'get_element',
    'checkbox_value_is', 'checkbox_toggle', 'checkbox_set', 'is_link',
    'is_button', 'button_click', 'link_click', 'is_textfield',
    'textfield_write'
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


def is_checkbox(the_id):
    elem = _get_elem(the_id)
    _elem_is_type(elem, the_id, 'checkbox')
    return elem


# Asserts that the value 'is' what the test says it is
def checkbox_value_is(chk_name, value):
    checkbox = is_checkbox(chk_name)
    real = checkbox.is_selected()
    msg = 'Checkbox: %r - Has Value: %r' % (chk_name, real)
    if real != value:
        _raise(msg)


def checkbox_toggle(chk_name):
    checkbox = is_checkbox(chk_name)
    before = checkbox.is_selected()
    checkbox.toggle()
    after = checkbox.is_selected()
    msg = 'Checkbox: %r - was not toggled, value remains: %r' % (chk_name, before)
    if before == after:
        _raise(msg)


def checkbox_set(chk_name, new_value):
    checkbox = is_checkbox(chk_name)
    # There is no method to 'unset' a checkbox in the browser object
    current_value = checkbox.is_selected()
    if new_value != current_value:
        checkbox_toggle(chk_name)


def is_textfield(the_id):
    elem = _get_elem(the_id)
    _elem_is_type(elem, the_id, 'text', 'password')
    return elem


def textfield_write(the_id, new_text):
    textfield = is_textfield(the_id)
    textfield.send_keys(new_text)
    current_text = textfield.get_value()
    msg = 'Textfield: %r - did not write' % the_id
    if current_text != new_text:
        _raise(msg)


def is_link(the_id):
    link = _get_elem(the_id)
    try:
        href = link.get_attribute('href')
    except NoSuchAttributeException:
        msg = 'Element %r is not a link' % the_id
        _raise(msg)
    return link


def link_click(the_id):
    link = is_link(the_id)
    link_url = link.get_attribute('href')
    link.click()
    url_is(link_url)
# Code for use with future wait_for (possibly also update url_is to return a boolean)
#    def url_match():
#        return browser.get_current_url() == link_url
#
#    waitfor(url_match, 'Page to load - Current URL: %r - Link URL: %r' % (browser.get_current_url(), link_url))


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
    if isinstance(the_id, WebElement):
        return the_id
    try:
        return browser.find_element_by_id(the_id)
    except NoSuchElementException:
        msg = 'Element %r does not exist' % the_id
        _raise(msg)

# Takes an optional 2nd input type for cases where types are similar
def _elem_is_type(elem, name, elem_type, opt_elem_type='none'):
    msg = 'Element %r is not a %r' % (name, elem_type)
    try:
        result = elem.get_attribute('type')
    except NoSuchAttributeException:
        _raise(msg)
    if not result == elem_type and not result == opt_elem_type :
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


def radio_select(the_id):
    elem = is_radio(the_id)
    elem.set_selected()


def text_is(the_id, text):
    elem = _get_elem(the_id)
    real = elem.get_text()
    msg = 'Element %r should have had text: %r\nIt has: %r' % (the_id, text,
                                                                real)
    if real != text:
        _raise(msg)


def get_element(tag=None, css_class=None, id=None, **kwargs):
    selector_string = ''
    if tag is not None:
        selector_string = tag
    if css_class is not None:
        selector_string += ('.%s' % (css_class,))
    if id is not None:
        selector_string += ('#%s' % (id,))

    selector_string += ''.join(['[%s=%r]' % (key, value) for
                                key, value in kwargs.items()])

    if not selector_string:
        msg = "Could not identify element: no arguments provided"
        _raise(msg)
    elements = browser._find_elements_by("css selector", selector_string)
    if len(elements) != 1:
        msg = "Couldn't identify element: %s elements found" % (len(elements),)
        _raise(msg)
    return elements[0]


def is_button(the_id):
    elem = _get_elem(the_id)
    _elem_is_type(elem, the_id, 'submit')
    return elem


def button_click(the_id):
    button = is_button(the_id)
    button.click()
