from sst.actions import *


go_to('http://www.google.com/')
assert_title_contains('Google')

set_base_url('http://www.google.com/')
go_to('/finance')

assert_url('/finance')
fails(assert_url, '/foo')

assert_title_contains('Google Finance: Stock market')

write_textfield(get_element(name='q'), 'IBM')
click_button(get_element(tag='input', value='Get quotes'))

assert_url_contains('IBM')