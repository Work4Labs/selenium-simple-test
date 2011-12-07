from sst.actions import *


# vars from data_driven_form.csv are available in namespace
assert('textfield1' in dir())
assert('password1' in dir())
assert('list_field' in dir())
assert(len(list_field) > 1)
assert((list_field[0] == 1) or (list_field[0] == 'a'))
assert isinstance(should_pass, bool)

go_to('/')
assert_title('The Page Title')
write_textfield(get_element(name='textfield1'), textfield1) # textfield1 comes from the associated csv data file
write_textfield(get_element(name='password1'), password1)
click_button(get_element(tag='input', value='Begin'))
assert_title('The Next Page')

