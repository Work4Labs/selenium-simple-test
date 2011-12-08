from sst.actions import *

# tests for assert_text, text_contains

go_to('/')

title = get_element(tag='title')
assert_text(title, 'The Page Title')
assert_text_contains(title, 'The Page')
fails(assert_text_contains, title, 'foobar')

body = get_element(tag='body')
assert_text_contains(body, '.*[C|c]ountry.*', regex=True)
