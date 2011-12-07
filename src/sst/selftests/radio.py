from sst.actions import *

go_to('/')

assert_radio('radio_with_id_1')
assert_radio(get_element(id='radio_with_id_1'))
fails(assert_radio, 'does not exist')
fails(assert_radio, 'headline')

assert_radio_value('radio_with_id_1', True)
assert_radio_value(get_element(id='radio_with_id_1'), True)
fails(assert_radio_value, 'radio_with_id_1', False)
fails(assert_radio_value, 'headline', True)

assert_radio_value('radio_with_id_2', False)
fails(assert_radio_value, 'radio_with_id_2', True)

set_radio_value('radio_with_id_1')
assert_radio_value('radio_with_id_1', True)
assert_radio_value('radio_with_id_2', False)

set_radio_value('radio_with_id_2')
assert_radio_value('radio_with_id_1', False)
assert_radio_value('radio_with_id_2', True)

set_radio_value(get_element(id='radio_with_id_1'))
assert_radio_value('radio_with_id_1', True)
assert_radio_value('radio_with_id_2', False)

fails(set_radio_value, 'does not exist')
fails(set_radio_value, 'headline')

assert_text('label1', 'First')
fails(assert_text, 'label1', 'the wrong text')
fails(assert_text, 'does not exist', 'does not matter')
fails(assert_text, 'radio_with_id_1', 'has no text')
