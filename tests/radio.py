from funcrunner.actions import *

goto('/')

is_radio('radio_with_id_1')
fails(is_radio, 'does not exist')
fails(is_radio, 'headline')

