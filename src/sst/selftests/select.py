from sst.actions import *

goto('/')

is_select('select_with_id_1')
is_select(get_element(id='select_with_id_1'))
fails(is_select, 'fake_id')
fails(is_select, 'headline')

set_select('select_with_id_1', 'Select Two')
select_value_is('select_with_id_1', 'Select Two')

'''The following should fail saying that the option is not set to the expected value'''
fails(select_value_is, 'select_with_id_1', 'Fake Text')
'''The following should fail saying that the option does not exist'''
fails(set_select, 'select_with_id_1', 'Fake Text')

