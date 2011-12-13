from sst.actions import *

go_to('/')

assert assert_element(id='select_with_id_1')
assert assert_element(css_class='unique_class', id='some_id')
assert assert_element(name='longscroll', href='/longscroll')
