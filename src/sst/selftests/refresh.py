from sst.actions import *

go_to('/')

assert_title('The Page Title')
assert_url('/')

refresh()

assert_title('The Page Title')
assert_url('/')
