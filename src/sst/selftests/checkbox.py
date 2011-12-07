from sst.actions import *

go_to('/')

assert_checkbox('id_sreg_country')
assert_checkbox(get_element(id='id_sreg_country'))

# fails for non existent element
fails(assert_checkbox, 'foobar')
# fails for element that exists but isn't a checkbox
fails(assert_checkbox, 'radio_with_id_1')

assert_checkbox_value('id_sreg_country', False)
assert_checkbox_value(get_element(id='id_sreg_country'), False)

# fails when given the wrong value
fails(assert_checkbox_value, 'id_sreg_country', True)

toggle_checkbox('id_sreg_country')
assert_checkbox_value('id_sreg_country', True)

toggle_checkbox('id_sreg_country')
assert_checkbox_value('id_sreg_country', False)

# restore checkbox to True for next tests
toggle_checkbox('id_sreg_country')

set_checkbox_value('id_sreg_country', False)
assert_checkbox_value('id_sreg_country', False)

set_checkbox_value('id_sreg_country', True)
assert_checkbox_value('id_sreg_country', True)

# check doesn't fail when setting check box to
# the same value as it already is
set_checkbox_value('id_sreg_country', True)
assert_checkbox_value('id_sreg_country', True)
