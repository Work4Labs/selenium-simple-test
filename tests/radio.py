from funcrunner.actions import *

goto('/')

is_radio('radio_with_id_1')
is_radio(get_element(id='radio_with_id_1'))
fails(is_radio, 'does not exist')
fails(is_radio, 'headline')

radio_value_is('radio_with_id_1', True)
radio_value_is(get_element(id='radio_with_id_1'), True)
fails(radio_value_is, 'radio_with_id_1', False)
fails(radio_value_is, 'headline', True)

radio_value_is('radio_with_id_2', False)
fails(radio_value_is, 'radio_with_id_2', True)

radio_select('radio_with_id_1')
radio_value_is('radio_with_id_1', True)
radio_value_is('radio_with_id_2', False)

radio_select('radio_with_id_2')
radio_value_is('radio_with_id_1', False)
radio_value_is('radio_with_id_2', True)

radio_select(get_element(id='radio_with_id_1'))
radio_value_is('radio_with_id_1', True)
radio_value_is('radio_with_id_2', False)

fails(radio_select, 'does not exist')
fails(radio_select, 'headline')

text_is('label1', 'First')
fails(text_is, 'label1', 'the wrong text')
fails(text_is, 'does not exist', 'does not matter')
fails(text_is, 'radio_with_id_1', 'has no text')
