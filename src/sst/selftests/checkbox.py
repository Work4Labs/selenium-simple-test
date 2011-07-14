from sst.actions import *

goto('/')

is_checkbox('id_sreg_country')
is_checkbox(get_element(id='id_sreg_country'))

# fails for non existent element
fails(is_checkbox, 'foobar')
# fails for element that exists but isn't a checkbox
fails(is_checkbox, 'radio_with_id_1')

checkbox_value_is('id_sreg_country', False)
checkbox_value_is(get_element(id='id_sreg_country'), False)

# fails when given the wrong value
fails(checkbox_value_is, 'id_sreg_country', True)

checkbox_toggle('id_sreg_country')
checkbox_value_is('id_sreg_country', True)

checkbox_toggle('id_sreg_country')
checkbox_value_is('id_sreg_country', False)

# restore checkbox to True for next tests
checkbox_toggle('id_sreg_country')

checkbox_set('id_sreg_country', False)
checkbox_value_is('id_sreg_country', False)

checkbox_set('id_sreg_country', True)
checkbox_value_is('id_sreg_country', True)

# check doesn't fail when setting check box to
# the same value as it already is
checkbox_set('id_sreg_country', True)
checkbox_value_is('id_sreg_country', True)
