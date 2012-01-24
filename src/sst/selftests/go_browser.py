from sst.actions import *

# navigate to populate history
go_to('/')
click_element('the_band_link')
assert_url('/begin')
go_to('/')
assert_url('/')
click_element('the_band_link')
assert_url('/begin')

# go back in Browser history
go_back()
assert_url('/')
go_back()
assert_url('/begin')
go_back()
assert_url('/')
