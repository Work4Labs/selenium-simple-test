from sst.actions import *

go_to('/')

elem = get_element(tag='body')
assert_css_property(elem, 'font-family', 'Ubuntu,Tahoma,sans-serif')

elem = get_element(tag='body')
assert_css_property(elem, 'font-family', 'Ubuntu', regex=True)

elems = get_elements(tag='h2')
for elem in elems:
    assert_css_property(elem, 'padding-left', '8px')

elems = get_elements(tag='h2')
for elem in elems:
    fails(assert_css_property, elem, 'padding-left', '999px')
