"""
The standard actions
====================

Tests comprise of python scripts in a "tests" directory. Files whose names
begin with an underscore will *not* be executed as test scripts.

Test scripts drive the browser through selenium by importing and using
actions.

The standard set of actions are imported by starting the test scripts with::

    from funcrunner.actions import *


Actions that work on page elements usually take either an element id or an
element object as their first argument. If the element you are working with
doesn't have a specific id you can get the element object with the
`get_element` action. `get_element` allows you to find an element by its
tagname, text, class or other attributes. See the `get_element` documentation.
"""

import re
import time

try:
    from selenium import webdriver
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.common.exceptions import (
        NoSuchElementException, NoSuchAttributeException,
        InvalidElementStateException, WebDriverException
    )
except ImportError as e:
    import sys
    print 'Error importing Selenium/Webdriver.  Selenium 2.x python bindings are required.'
    print e
    sys.exit(1)


__all__ = [
    'start', 'stop', 'title_is', 'title_contains', 'goto', 'waitfor', 'fails', 'url_is',
    'is_radio', 'set_base_url', 'reset_base_url', 'radio_value_is',
    'radio_select', 'text_is', 'is_checkbox', 'get_element',
    'checkbox_value_is', 'checkbox_toggle', 'checkbox_set', 'is_link',
    'is_button', 'button_click', 'link_click', 'is_textfield',
    'textfield_write', 'url_contains', 'sleep', 'is_select', 
    'select_value_is', 'set_select', 'get_link_url'
]


browser = None

BASE_URL = 'http://localhost:8000/'
__DEFAULT_BASE_URL__ = BASE_URL
VERBOSE = True

sleep = time.sleep


def _raise(msg):
    _print(msg)
    raise AssertionError(msg)


def set_base_url(url):
    """Set the url used for relative arguments to the `goto` action."""
    global BASE_URL
    BASE_URL = url


def reset_base_url():
    """
    Restore the base url to the default. This is called automatically for
    you when a test script completes."""
    global BASE_URL
    BASE_URL = __DEFAULT_BASE_URL__


def _print(text):
    if VERBOSE:
        print text


def start():
    """
    Starts Firefox with a new browser session. Called for you at the start of
    each test script."""
    global browser
    _print('\nStarting browser')
    browser = webdriver.Firefox()


def stop():
    """
    Stops Firefox and ends the browser session. Called automatically for you at
    the end of each test script."""
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
    """
    Goto a specific URL. If the url provided is a relative url it will be added
    to the base url. You can change the base url for the test with
    `set_base_url`."""
    url = _fix_url(url)
    _print('Going to... %s' % url)
    browser.get(url)


def is_checkbox(the_id):
    """
    Assert that the element is a checkbox. Takes an id or an element object.
    Raises a failure exception if the element specified doesn't exist or isn't
    a checkbox."""
    elem = _get_elem(the_id)
    _elem_is_type(elem, the_id, 'checkbox')
    return elem


def checkbox_value_is(chk_name, value):
    """
    Assert checkbox value. Takes an element id or object plus either True or
    False. Raises a failure exception if the element specified doesn't exist
    or isn't a checkbox."""
    checkbox = is_checkbox(chk_name)
    real = checkbox.is_selected()
    msg = 'Checkbox: %r - Has Value: %r' % (chk_name, real)
    if real != value:
        _raise(msg)


def checkbox_toggle(chk_name):
    """
    Toggle the checkbox value. Takes an element id or object. Raises a failure
    exception if the element specified doesn't exist or isn't a checkbox."""
    checkbox = is_checkbox(chk_name)
    before = checkbox.is_selected()
    checkbox.toggle()
    after = checkbox.is_selected()
    msg = 'Checkbox: %r - was not toggled, value remains: %r' % (chk_name, before)
    if before == after:
        _raise(msg)


def checkbox_set(chk_name, new_value):
    """
    Set a checkbox to a specific value, either True or False. Raises a failure
    exception if the element specified doesn't exist or isn't a checkbox."""
    checkbox = is_checkbox(chk_name)
    # There is no method to 'unset' a checkbox in the browser object
    current_value = checkbox.is_selected()
    if new_value != current_value:
        checkbox_toggle(chk_name)


def is_textfield(the_id):
    """
    Assert that the element is a textfield, textarea or password box. Takes an
    id or an element object. Raises a failure exception if the element
    specified doesn't exist or isn't a textfield."""
    elem = _get_elem(the_id)
    _elem_is_type(elem, the_id, 'text', 'password', 'textarea')
    return elem


def textfield_write(the_id, new_text, check=True):
    """
    Set the specified text into the textfield. If the text fails to write (the
    textfield contents after writing are different to the specified text) this
    function will fail. You can switch off the checking by passing
    `check=False`."""
    textfield = is_textfield(the_id)
    textfield.clear()
    textfield.send_keys(new_text)
    if not check:
        return
    current_text = textfield.get_attribute('value')
    msg = 'Textfield: %r - did not write. Text was: %r' % (the_id, current_text)
    if current_text != new_text:
        _raise(msg)


def is_link(the_id):
    """
    Assert that the element is a link."""
    link = _get_elem(the_id)
    href = link.get_attribute('href')
    if href is None:
        msg = 'The text %r is not part of a Link or a Link ID' % the_id
        _raise(msg)  
    return link


def get_link_url(the_id):
    """
    Return the URL from a link."""
    link = is_link(the_id)
    link_url = link.get_attribute('href')
    return link_url


def link_click(the_id, check=False):
    """
    Click the specified link. As some links do redirects the location you end
    up at is not checked by default. If you pass in `check=True` then this
    action asserts that the resulting url is the link url."""
    link = is_link(the_id)
    link_url = link.get_attribute('href')
    link.click()

    # some links do redirects - so we
    # don't check by default
    if check:
        url_is(link_url)


# Code for use with future wait_for (possibly also update url_is to return a boolean)
#    def url_match():
#        return browser.get_current_url() == link_url
#
#    waitfor(url_match, 'Page to load - Current URL: %r - Link URL: %r' % (browser.get_current_url(), link_url))


def title_is(title):
    """Assert the page title is as specified."""
    real_title = browser.title
    msg = 'Title is: %r. Should be: %r' % (real_title, title)
    if not real_title == title:
        _raise(msg)


def title_contains(title):
    """Assert the page title containts the specified text."""
    real_title = browser.title
    msg = 'Title is: %r. Does not contain %r' % (real_title, title)
    if not re.search(title, real_title):
        _raise(msg)
        
        
def url_is(url):
    """Assert the current url is as specified. Can be an absolute url or
    relative to the base url."""
    url = _fix_url(url)
    real_url = browser.current_url
    msg = 'Url is: %r\nShould be: %r' % (real_url, url)
    if not url == real_url:
        _raise(msg)


def url_contains(url):
    """Assert the current url contains the specified text."""
    real_url = browser.current_url
    if not re.search(url, real_url):
        _raise('url is %r. Does not contain %r' % (real_url, url))


"""
# Example action using waitfor
def wait_for_title_to_change(title):
    def title_changed():
        return browser.title == title

    waitfor(title_changed, 'title to change')
"""

def waitfor(condition, msg='', timeout=5, poll=0.1):
    """
    Wait for an action to pass. Useful for checking the results of actions that
    may take some time to complete. This action takes a condition function
    and calls it until it returns True. The maximum amount of time it will wait
    is specified as the timeout (default 5 seconds). The function is called at
    intervals specified by the poll argument (default every 0.1 seconds).

    If it fails, the condition function never returns True before the timeout,
    then any msg you supply will be added to the failure message.

    An example action using waitfor::

        def wait_for_title_to_change(title):
            def title_changed():
                return browser.title == title

            waitfor(title_changed, 'title to change')

    XXXX Note that test scripts shouldn't use the browser object directly,
    so if waitfor is to be used in test scripts (instead of for building
    actions) it should be changed to catch assertion errors instead of condition
    functions that return True or False.
    """
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


def _get_elem(the_id):
    if isinstance(the_id, WebElement):
        return the_id
    try:
        return browser.find_element_by_id(the_id)
    except NoSuchElementException:
        msg = 'Element with id: %r does not exist' % the_id
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


def is_select(the_id):
    """Assert the specified element is a select drop-list"""
    elem = _get_elem(the_id)
    _elem_is_type(elem, the_id, 'select-one')
    return elem


def set_select(the_id, text_in):
    """Set the select drop list to a text value provided to the function"""
    elem = is_select(the_id)
    for element in elem.find_elements_by_tag_name('option'):
        if element.text == text_in:
            element.select()
            return
    msg = 'The following option could not be found in the list: %s' % text_in 
    _raise(msg)
    

def select_value_is(the_id, text_in):
    """Assert the specified element is a select list with the specified value"""
    elem = is_select(the_id)
    # Because there is no way to connect the current text of a select element we have to use 'value' 
    current = elem.get_attribute('value')
    for element in elem.find_elements_by_tag_name("option"):
        if text_in == element.text and current == element.get_attribute('value'):
            return 
    msg = 'The option is not currently set to the following expected value: %s' % text_in 
    _raise(msg)
    

def is_radio(the_id):
    """Assert the specified element is a radio button"""
    elem = _get_elem(the_id)
    _elem_is_type(elem, the_id, 'radio')
    return elem


def radio_value_is(the_id, value):
    """Assert the specified element is a radio button with the specified value;
    True for selected and False for unselected."""
    elem = is_radio(the_id)
    selected = elem.is_selected()
    msg = 'Radio %r should be set to: %s.' % (the_id, value)
    if value != selected:
        _raise(msg)

def radio_select(the_id):
    """Select the specified radio button."""
    elem = is_radio(the_id)
    elem.select()


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


def text_is(the_id, text):
    """Assert the specified element has the specified text."""
    elem = _get_elem(the_id)
    real = _get_text(elem)
    if real is None:
        msg = "Element %r has no text attribute"
        _raise(msg)

    if real != text:
        msg = 'Text should be %r.\nIt is %r.' % (text, real)
        _raise(msg)


def _check_text(elem, text):
    return _get_text(elem) == text


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
    selector_string = ''
    if tag is not None:
        selector_string = tag
    if css_class is not None:
        selector_string += ('.%s' % (css_class,))
    if id is not None:
        selector_string += ('#%s' % (id,))

    selector_string += ''.join(['[%s=%r]' % (key, value) for
                                key, value in kwargs.items()])
    if text is not None and not selector_string:
        elements = browser.find_elements_by_xpath('//*[text() = %r]' % text)
    else:
        if not selector_string:
            msg = "Could not identify element: no arguments provided"
            _raise(msg)
        elements = browser.find_elements_by_css_selector(selector_string)

    if text is not None:
        # if text was specified, filter elements
        elements = [element for element in elements if _check_text(element, text)]
    if len(elements) != 1:
        msg = "Couldn't identify element: %s elements found" % (len(elements),)
        _raise(msg)
    return elements[0]


def is_button(the_id):
    """Assert that the specified element is a button."""
    elem = _get_elem(the_id)
    _elem_is_type(elem, the_id, 'submit')
    return elem


def button_click(the_id):
    """Click the specified button."""
    button = is_button(the_id)
    button.click()
