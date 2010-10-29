from funcrunner.actions import *

goto('/')

checkbox_value_is('id_sreg_country', False)
checkbox_toggle('id_sreg_country')
checkbox_set('id_sreg_country', False)
checkbox_set('id_sreg_country', True)
checkbox_set('id_sreg_country', True)
