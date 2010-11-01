from funcrunner.actions import *

goto('/')

is_checkbox('id_sreg_country')
is_checkbox(get_element(id='id_sreg_country'))
fails(is_checkbox, 'foobar')
fails(is_checkbox, 'radio_with_id_1')

checkbox_value_is('id_sreg_country', False)
checkbox_value_is(get_element(id='id_sreg_country'), False)

# fails when given the wrong value
fails(checkbox_value_is, 'id_sreg_country', True)

# fails for non existent element
fails(checkbox_value_is, 'foobar', True)

# fails for element that exists but isn't a checkbox
fails(checkbox_value_is, 'radio_with_id_1', True)

checkbox_toggle('id_sreg_country')
checkbox_set('id_sreg_country', False)
checkbox_set('id_sreg_country', True)
checkbox_set('id_sreg_country', True)
