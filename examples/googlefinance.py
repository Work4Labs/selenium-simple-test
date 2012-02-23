from sst.actions import *


set_base_url('http://www.google.com/')

go_to('/')
assert_title_contains('Google')

go_to('/finance')
assert_url('/finance')
assert_title_contains('Google Finance: Stock market')

write_textfield(get_element(name='q'), 'IBM')
click_button('gbqfb')
assert_url_contains('IBM')
assert_title_contains('International Business Machines')
