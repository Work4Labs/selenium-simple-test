from sst.actions import *


goto('http://www.google.com/')
title_contains('Google')

set_base_url('http://www.google.com/')
goto('/finance')

url_is('/finance')
fails(url_is, '/foo')

title_contains('Google Finance: Stock market')

textfield_write(get_element(name='q'), 'IBM')
button_click(get_element(tag='input', value='Get quotes'))

url_contains('IBM')