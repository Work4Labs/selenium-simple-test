from sst.actions import *


go_to('http://finance.search.yahoo.com/')
assert_title_contains('Yahoo!')
element = get_element(id='yschsp')
write_textfield(element, 'AMZN', clear=False)
element = get_element(id='yschbt')
click_button(element)
assert_title_contains('AMZN - Yahoo')
