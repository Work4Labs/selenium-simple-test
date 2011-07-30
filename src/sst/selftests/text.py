from sst.actions import *

# tests for text_is, text_contains

goto('/')

title = get_element(tag='title')
text_is(title, 'The Page Title')
text_contains(title, 'The Page')

body = get_element(tag='body')
text_contains(body, '.*[C|c]ountry.*')
