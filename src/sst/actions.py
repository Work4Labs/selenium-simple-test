#!/usr/bin/env python
#
#   Copyright (c) 2011 Canonical Ltd.
#
#   This file is part of: SST (selenium-simple-test)
#   https://launchpad.net/selenium-simple-test
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#


"""
Tests are comprised of Python scripts in a "tests" directory. Files whose names
begin with an underscore will *not* be executed as test scripts.

Test scripts drive the browser through selenium/webdriver by importing and using
actions.

The standard set of actions are imported by starting the test scripts with::

    from sst.actions import *


Actions that work on page elements usually take either an element id or an
element object as their first argument. If the element you are working with
doesn't have a specific id you can get the element object with the
`get_element` action. `get_element` allows you to find an element by its
tagname, text, class or other attributes. See the `get_element` documentation.
"""


import os
import re
import time

from pdb import set_trace as debug

from sst import config

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    NoSuchElementException, NoSuchAttributeException,
    InvalidElementStateException, WebDriverException
)

from unittest2 import SkipTest


__all__ = [
    'start', 'stop', 'title_is', 'title_contains', 'goto', 'waitfor', 'fails',
    'is_radio', 'set_base_url', 'reset_base_url', 'radio_value_is',
    'radio_select', 'text_is', 'text_contains', 'is_checkbox', 'get_element',
    'get_elements', 'checkbox_value_is', 'checkbox_toggle', 'checkbox_set',
    'is_link', 'is_button', 'button_click', 'link_click', 'is_textfield',
    'textfield_write', 'url_contains', 'url_is', 'sleep', 'is_select',
    'select_value_is', 'set_select', 'get_link_url', 'exists_element',
    'set_wait_timeout', 'get_argument', 'run_test', 'get_base_url',
    'end_test', 'skip', 'get_element_by_css', 'get_elements_by_css',
    'take_screenshot', 'debug', 'get_page_source', 'simulate_keys',
    'element_click',
]


browser = None

BASE_URL = 'http://localhost:8000/'
__DEFAULT_BASE_URL__ = BASE_URL
VERBOSE = True


class EndTest(StandardError):
    pass


debug.__doc__ = """Start the debugger (a shortcut for `pdb.set_trace()`."""


class _Sentinel(object):
    def __repr__(self):
        return 'default'
_sentinel = _Sentinel()



def _raise(msg):
    _print(msg)
    raise AssertionError(msg)


def set_base_url(url):
    """Set the url used for relative arguments to the `goto` action."""
    global BASE_URL
    if not url.endswith('/'):
        url += '/'
    if not url.startswith('http'):
        url = 'http://' + url
    _print('Setting base url to: %s' % url)
    BASE_URL = url


def get_base_url():
    """Return the base url used by `goto`."""
    return BASE_URL


def reset_base_url():
    """
    Restore the base url to the default. This is called automatically for
    you when a test script completes."""
    global BASE_URL
    BASE_URL = __DEFAULT_BASE_URL__


def end_test():
    """
    If called it ends the test. Can be used conditionally to exit a
    test under certain conditions."""
    raise EndTest


def skip(reason=''):
    """
    Skip the test. Unlike `end_test` a skipped test will be reported
    as a skip rather than a pass."""
    raise SkipTest(reason)


def _print(text):
    if VERBOSE:
        print text


def start(browser_type=None, browser_version='',
          browser_platform='ANY', session_name='',
          javascript_disabled=False, webdriver_remote=None):
    """
    Starts Browser with a new session. Called for you at
    the start of each test script."""
    global browser

    if browser_type is None:
        browser_type = config.browser_type

    _print('\nStarting %s:' % browser_type)
    if webdriver_remote is None:
        profile = getattr(webdriver, '%sProfile' % browser_type)()

        if browser_type == 'Firefox':
            profile.set_preference('intl.accept_languages', '"en"')

        if javascript_disabled:
            profile.set_preference('javascript.enabled', False)

        browser = getattr(webdriver, browser_type)(profile)
    else:
        desired_capabilities = {"browserName": browser_type.lower(),
                                "platform": browser_platform.upper(),
                                "version": browser_version,
                                "javascriptEnabled": not javascript_disabled,
                                "name": session_name}
        browser = webdriver.Remote(desired_capabilities=desired_capabilities,
                                   command_executor=webdriver_remote)


def stop():
    """
    Stops Firefox and ends the browser session. Called automatically for you at
    the end of each test script."""
    global browser
    _print('Stopping browser')
    # quit calls close() and does cleanup
    browser.quit()
    browser = None


def take_screenshot(filename='screenshot.png'):
    """
    Takes a screenshot of the browser window. Called automatically on failures
    when running in `-s` mode."""
    _print('Capturing Screenshot')
    _make_results_dir()
    screenshot_file = os.path.join(config.results_directory, filename)
    browser.get_screenshot_as_file(screenshot_file)


def _make_results_dir():
    """
    Make results directory if it does not exist."""
    try:
        os.makedirs(config.results_directory)
    except OSError:
        pass  # already exists


def sleep(secs):
    """
    Delay execution for a given number of seconds. The argument may be a floating
    point number for subsecond precision."""
    time.sleep(secs)


def _fix_url(url):
    if url.startswith('/'):
        url = url[1:]
    if not url.startswith('http'):
        url = BASE_URL + url
    return url



def get_argument(name, default=_sentinel):
    """
    Get an argument from the one the test was called with.

    A test is called with arguments when it is executed by
    the `run_test`. You can optionally provide a default value
    that will be used if the argument is not set. If you don't
    provide a default value and the argument is missing an
    exception will be raised."""
    args = config.__args__

    value = args.get(name, default)
    if value is _sentinel:
        raise LookupError(name)
    return value


def run_test(name, **kwargs):
    """
    Execute a named test, with the specified arguments.

    Arguments can be retrieved by the test with `get_argument`.

    The `name` is the test file name without the '.py'.

    You can specify tests in an alternative directory with
    relative path syntax. e.g.::

        run_test('subdir/foo', spam='eggs')

    Tests can return a result by setting the name `RESULT`
    in the test.

    Tests are executed with the same browser (and browser
    session) as the test calling `test_run`. This includes
    whether or not Javascript is enabled.

    Before the test is called the timeout and base url are
    reset, but will be restored to their orginal value
    when `run_test` returns."""
    # delayed import to workaround circular imports
    from sst import context
    _print('Executing test: %s' % name)
    return context.run_test(name, kwargs)


def goto(url=''):
    """
    Goto a specific URL. If the url provided is a relative url it will be added
    to the base url. You can change the base url for the test with
    `set_base_url`."""
    url = _fix_url(url)
    _print('Going to... %s' % url)
    browser.get(url)


def is_checkbox(id_or_elem):
    """
    Assert that the element is a checkbox. Takes an id or an element object.
    Raises a failure exception if the element specified doesn't exist or isn't
    a checkbox."""
    elem = _get_elem(id_or_elem)
    _elem_is_type(elem, id_or_elem, 'checkbox')
    return elem


def checkbox_value_is(id_or_elem, value):
    """
    Assert checkbox value. Takes an element id or object plus either True or
    False. Raises a failure exception if the element specified doesn't exist
    or isn't a checkbox."""
    checkbox = is_checkbox(id_or_elem)
    real = checkbox.is_selected()
    msg = 'Checkbox: %r - Has Value: %r' % (id_or_elem, real)
    if real != value:
        _raise(msg)


def checkbox_toggle(id_or_elem):
    """
    Toggle the checkbox value. Takes an element id or object. Raises a failure
    exception if the element specified doesn't exist or isn't a checkbox."""
    _print('Toggling checkbox: %r' % id_or_elem)
    checkbox = is_checkbox(id_or_elem)
    before = checkbox.is_selected()
    checkbox.click()
    after = checkbox.is_selected()
    msg = 'Checkbox: %r - was not toggled, value remains: %r' % (id_or_elem, before)
    if before == after:
        _raise(msg)


def checkbox_set(id_or_elem, new_value):
    """
    Set a checkbox to a specific value, either True or False. Raises a failure
    exception if the element specified doesn't exist or isn't a checkbox."""
    _print('Setting checkbox %r to %s' % (id_or_elem, new_value))
    checkbox = is_checkbox(id_or_elem)
    # There is no method to 'unset' a checkbox in the browser object
    current_value = checkbox.is_selected()
    if new_value != current_value:
        checkbox_toggle(id_or_elem)


def _make_keycode(key_to_make):
    """
    Take a key and return a keycode"""
    k = keys.Keys()
    keycode = k.__getattribute__(key_to_make.upper())
    return keycode


def simulate_keys(id_or_elem, key_to_press):
    """
    Simulate key sent to specified element.  (available keys located in `selenium/webdriver/common/keys.py`).
    
    e.g.::
    
        simulate_keys('text_1', 'BACK_SPACE')
        
    """
    key_element = _get_elem(id_or_elem)
    _print('Simulating keypress on %r with %r key' % (id_or_elem, key_to_press))
    key_code = _make_keycode(key_to_press)
    key_element.send_keys(key_code)


_textfields = (
    'text', 'password', 'textarea',
    'email', 'url', 'search', 'number'
)
def is_textfield(id_or_elem):
    """
    Assert that the element is a textfield, textarea or password box. Takes an
    id or an element object. Raises a failure exception if the element
    specified doesn't exist or isn't a textfield."""
    elem = _get_elem(id_or_elem)
    _elem_is_type(elem, id_or_elem, *_textfields)
    return elem
        
    
def textfield_write(id_or_elem, new_text, check=True):
    """
    Set the specified text into the textfield. If the text fails to write (the
    textfield contents after writing are different to the specified text) this
    function will fail. You can switch off the checking by passing
    `check=False`."""
    _print('Writing to textfield %r with text %r' % (id_or_elem, new_text))
    textfield = is_textfield(id_or_elem)
    textfield.clear()
    textfield.send_keys(new_text)
    if not check:
        return
    _print('Check text wrote correctly')
    current_text = textfield.get_attribute('value')
    msg = 'Textfield: %r - did not write. Text was: %r' % (id_or_elem, current_text)
    if current_text != new_text:
        _raise(msg)


def is_link(id_or_elem):
    """Assert that the element is a link."""
    link = _get_elem(id_or_elem)
    href = link.get_attribute('href')
    if href is None:
        msg = 'The text %r is not part of a Link or a Link ID' % id_or_elem
        _raise(msg)
    return link


def get_link_url(id_or_elem):
    """Return the URL from a link."""
    _print('Getting url from link %r' % id_or_elem)
    link = is_link(id_or_elem)
    link_url = link.get_attribute('href')
    return link_url


def link_click(id_or_elem, check=False, wait=True):
    """
    Click the specified link. As some links do redirects the location you end
    up at is not checked by default. If you pass in `check=True` then this
    action asserts that the resulting url is the link url.

    By default this action will wait until a page with a body element is
    available fter the click. You can switch off this behaviour by passing
    `wait=False`."""
    _print('Clicking link %r' % id_or_elem)
    link = is_link(id_or_elem)
    link_url = link.get_attribute('href')
    link.click()

    if wait:
        _waitforbody()

    # some links do redirects - so we
    # don't check by default
    if check:
        url_is(link_url)

def element_click(id_or_elem, wait=True):
    """
    Click on an element of any kind not specific to links or buttons.

    By default this action will wait until a page with a body element is
    available after the click. You can switch off this behaviour by passing
    `wait=False`."""

    _print('Clicking element %r' % id_or_elem)
    id_or_elem.click()

    if wait:
        _waitforbody()


def title_is(title):
    """Assert the page title is as specified."""
    real_title = browser.title
    msg = 'Title is: %r. Should be: %r' % (real_title, title)
    if real_title != title:
        _raise(msg)


def title_contains(text, regex=False):
    """Assert the page title contains the specified text (or regex pattern)."""
    real_title = browser.title
    msg = 'Title is: %r. Does not contain %r' % (real_title, text)
    if regex:
        if not re.search(text, real_title):
            _raise(msg)
    else:
        if not text in real_title:
            _raise(msg)


def url_is(url):
    """
    Assert the current url is as specified. Can be an absolute url or
    relative to the base url."""
    url = _fix_url(url)
    real_url = browser.current_url
    msg = 'Url is: %r\nShould be: %r' % (real_url, url)
    if url != real_url:
        _raise(msg)


def url_contains(text, regex=False):
    """Assert the current url contains the specified text (regex pattern)."""
    real_url = browser.current_url
    msg = 'Url is %r.\nDoes not contain %r' % (real_url, text)
    if regex:
        if not re.search(text, real_url):
            _raise(msg)
    else:
        if text not in real_url:
            _raise(msg)


_TIMEOUT = 10
_POLL = 0.1

def set_wait_timeout(timeout, poll=None):
    """
    Set the timeout, in seconds, used by`waitfor`. The default at the start of
    a test is always 10 seconds.

    The optional second argument, is how long (in seconds) `waitfor` should
    wait in between checking its condition (the poll frequency). The default
    at the start of a test is always 0.1 seconds."""
    global _TIMEOUT
    global _POLL
    _TIMEOUT = timeout
    msg = 'Setting wait timeout to %rs' % timeout
    if poll is not None:
        msg += ('. Setting poll time to %rs' % poll)
        _POLL = poll
    _print(msg)


def _get_name(obj):
    try:
        return obj.__name__
    except:
        return repr(obj)


def waitfor(condition, *args, **kwargs):
    """
    Wait for an action to pass. Useful for checking the results of actions that
    may take some time to complete.

    This action takes a condition function and any arguments it should be called
    with. The condition function can either be an action or a function that
    returns True for success and False for failure. For example::

        waitfor(title_is, 'Some page title')

    If the specified condition does not become true within 5 seconds then `waitfor`
    fails. You can set the timeout for `waitfor` by calling `set_wait_timeout`."""
    global VERBOSE
    _print('Waiting for %s' % _get_name(condition))

    original = VERBOSE
    VERBOSE = False
    try:
        max_time = time.time() + _TIMEOUT
        msg = condition.__name__
        while True:
            try:
                result = condition(*args, **kwargs)
            except AssertionError:
                pass
            else:
                if result != False:
                    break

            if time.time() > max_time:
                error = 'Timed out waiting for: ' + msg
                _raise(error)
            time.sleep(_POLL)
    finally:
        VERBOSE = original


def fails(action, *args, **kwargs):
    """
    This action is particularly useful for *testing* other actions, by
    checking that they fail when they should do. `fails` takes a function
    (usually an action) and any arguments and keyword arguments to call the
    function with. If calling the function raises an AssertionError then
    `fails` succeeds. If the function does *not* raise an AssertionError then
    this action raises the appropriate failure exception. Alll other
    exceptions will be propagated normally."""
    try:
        action(*args, **kwargs)
    except AssertionError:
        return
    msg = 'Action %r did not fail' % action.__name__
    _raise(msg)


def _get_elem(id_or_elem):
    if isinstance(id_or_elem, WebElement):
        return id_or_elem
    try:
        return browser.find_element_by_id(id_or_elem)
    except (NoSuchElementException, WebDriverException):
        msg = 'Element with id: %r does not exist' % id_or_elem
        _raise(msg)


# Takes an optional 2nd input type for cases like textfield & password
#    where types are similar
def _elem_is_type(elem, name, *elem_types):
    try:
        result = elem.get_attribute('type')
    except NoSuchAttributeException:
        msg = "Element has no type attribute"
        _raise(msg)
    if not result in elem_types:
        msg = 'Element %r is not one of %r' % (name, elem_types)
        _raise(msg)


def is_select(id_or_elem):
    """Assert the specified element is a select drop-list."""
    elem = _get_elem(id_or_elem)
    _elem_is_type(elem, id_or_elem, 'select-one')
    return elem


def set_select(id_or_elem, text_in):
    """Set the select drop list to a text value provided to the function."""
    _print('Setting %r option list to %s' % (id_or_elem, text_in))
    elem = is_select(id_or_elem)
    for element in elem.find_elements_by_tag_name('option'):
        if element.text == text_in:
            element.click()
            return
    msg = 'The following option could not be found in the list: %s' % text_in
    _raise(msg)


def select_value_is(id_or_elem, text_in):
    """Assert the specified element is a select list with the specified value."""
    elem = is_select(id_or_elem)
    # Because there is no way to connect the current text of a select element we have to use 'value'
    current = elem.get_attribute('value')
    for element in elem.find_elements_by_tag_name("option"):
        if text_in == element.text and current == element.get_attribute('value'):
            return
    msg = 'The option is not currently set to the following expected value: %s' % text_in
    _raise(msg)


def is_radio(id_or_elem):
    """Assert the specified element is a radio button."""
    elem = _get_elem(id_or_elem)
    _elem_is_type(elem, id_or_elem, 'radio')
    return elem


def radio_value_is(id_or_elem, value):
    """
    Assert the specified element is a radio button with the specified value;
    True for selected and False for unselected."""
    elem = is_radio(id_or_elem)
    selected = elem.is_selected()
    msg = 'Radio %r should be set to: %s.' % (id_or_elem, value)
    if value != selected:
        _raise(msg)


def radio_select(id_or_elem):
    """Select the specified radio button."""
    _print('Selecting radio button item %r' % id_or_elem)
    elem = is_radio(id_or_elem)
    elem.click()


def _get_text(elem):
    text = None
    try:
        text = elem.text
    except InvalidElementStateException:
        pass
    if text:
        # Note that some elements (like textfields) return empty string
        # for text and we still need to call value
        return text
    try:
        text = elem.get_attribute('value')
    except InvalidElementStateException:
        pass
    return text


def text_is(id_or_elem, text):
    """Assert the specified element text is as specified."""
    elem = _get_elem(id_or_elem)
    real = _get_text(elem)
    if real is None:
        msg = 'Element %r has no text attribute' % id_or_elem
        _raise(msg)
    if real != text:
        msg = 'Element text should be %r.\nIt is %r.' % (text, real)
        _raise(msg)


def text_contains(id_or_elem, text, regex=False):
    """Assert the specified element contains the specified text (regex pattern)."""
    elem = _get_elem(id_or_elem)
    real = _get_text(elem)
    if real is None:
        msg = 'Element %r has no text attribute' % id_or_elem
        _raise(msg)
    msg = 'Element text is %r. Does not contain %r' % (real, text)
    if regex:
        if not re.search(text, real):
            _raise(msg)
    else:
        if text not in real:
            _raise(msg)


def _check_text(elem, text):
    return _get_text(elem) == text


def get_elements(tag=None, css_class=None, id=None, text=None, **kwargs):
    """
    This function will find and return all matching elements by any of several
    attributes. If the elements cannot be found from the attributes you
    provide, the call will fail with an exception.

    You can specify as many or as few attributes as you like."""
    selector_string = ''
    if tag is not None:
        selector_string = tag
    if css_class is not None:
        selector_string += ('.%s' % (css_class,))
    if id is not None:
        selector_string += ('#%s' % (id,))

    selector_string += ''.join(['[%s=%r]' % (key, value) for
                                key, value in kwargs.items()])
    try:
        if text is not None and not selector_string:
            elements = browser.find_elements_by_xpath('//*[text() = %r]' % text)
        else:
            if not selector_string:
                msg = 'Could not identify element: no arguments provided'
                _raise(msg)
            elements = browser.find_elements_by_css_selector(selector_string)
    except (WebDriverException, NoSuchElementException) as e:
        msg = 'Element not found (%s)' % (e,)
        _raise(msg)

    if text is not None:
        # if text was specified, filter elements
        elements = [element for element in elements if _check_text(element, text)]

    if len(elements) == 0:
        msg = 'Could not identify elements: 0 elements found'
        _raise(msg)

    return elements


def get_element(tag=None, css_class=None, id=None, text=None, **kwargs):
    """
    This function will find and return an element by any of several
    attributes. If the element cannot be found from the attributes you
    provide, or the attributes match more than one element, the call will fail
    with an exception.

    Finding elements is useful for checking that the element exists, and also
    for passing to other actions that work with element objects.

    You can specify as many or as few attributes as you like, so long as they
    uniquely identify one element."""
    elements = get_elements(tag=tag, css_class=css_class, id=id, text=text, **kwargs)

    if len(elements) != 1:
        msg = 'Could not identify element: %s elements found' % len(elements)
        _raise(msg)

    return elements[0]


def exists_element(tag=None, css_class=None, id=None, text=None, **kwargs):
    """
    This function will find if an element exists by any of several
    attributes. It returns True if the element is found or False
    if it can't be found.

    You can specify as many or as few attributes as you like."""
    try:
        get_elements(tag=tag, css_class=css_class, id=id, text=text, **kwargs)
        return True
    except AssertionError:
        return False


def is_button(id_or_elem):
    """Assert that the specified element is a button."""
    elem = _get_elem(id_or_elem)
    if elem.tag_name == 'button':
        return elem
    _elem_is_type(elem, id_or_elem, 'submit')
    return elem


def button_click(id_or_elem, wait=True):
    """Click the specified button.

    By default this action will wait until a page with a body element is
    available fter the click. You can switch off this behaviour by passing
    `wait=False`."""
    _print('Clicking button %r' % id_or_elem)
    button = is_button(id_or_elem)
    button.click()

    if wait:
        _waitforbody()


def get_elements_by_css(selector):
    """Find all elements that match a css selector"""
    try:
        return browser.find_elements_by_css_selector(selector)
    except (WebDriverException, NoSuchElementException) as e:
        _raise('Error finding elements: (%s)' % (e,))


def get_element_by_css(selector):
    """Find an element by css selector."""
    elements = get_elements_by_css(selector)
    if len(elements) != 1:
        msg = 'Could not identify element: %s elements found' % len(elements)
        _raise(msg)
    return elements[0]


def _waitforbody():
    waitfor(get_element, tag='body')


def get_page_source():
    """Gets the source of the current page."""
    return browser.page_source
