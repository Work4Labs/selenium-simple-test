from sst.actions import *

go_to('/')

assert_dropdown('select_with_id_1')
assert_dropdown(get_element(id='select_with_id_1'))
fails(assert_dropdown, 'fake_id')
fails(assert_dropdown, 'headline')

set_dropdown_value('select_with_id_1', 'Select Two')
assert_dropdown_value('select_with_id_1', 'Select Two')

'''The following should fail saying that the option is not set to the expected value'''
fails(assert_dropdown_value, 'select_with_id_1', 'Fake Text')
'''The following should fail saying that the option does not exist'''
fails(set_dropdown_value, 'select_with_id_1', 'Fake Text')

