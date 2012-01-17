from sst.actions import *

go_to('/')

assert_element(id='select_with_id_1')
assert_element(css_class='unique_class', id='some_id')
assert_element(name='longscroll', href='/longscroll')

fails(assert_element, id='nonexistent')
fails(assert_element, css_class='unique_class', name='fish')
