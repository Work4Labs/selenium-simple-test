from funcrunner.actions import *

goto('/')

is_checkbox('id_sreg_country')
is_checkbox(get_element(id='id_sreg_country'))
fails(is_checkbox, 'foobar')

checkbox_value_is('id_sreg_country', False)
checkbox_value_is(get_element(id='id_sreg_country'), False)
fails(checkbox_value_is, 'id_sreg_country', True)

checkbox_toggle('id_sreg_country')
checkbox_set('id_sreg_country', False)
checkbox_set('id_sreg_country', True)
checkbox_set('id_sreg_country', True)
