from sst.actions import *


goto('/')
link_click('popup_link')

# switch to new window/tab
switch_to_window('_NEW_WINDOW')
title_is('Popup Window')

# switch back to default/main window/tab
switch_to_window()
title_is('The Page Title')

# switch to new window/tab
switch_to_window(window_name='_NEW_WINDOW')
title_is('Popup Window')

# switch back to default/main window/tab
switch_to_window('')
title_is('The Page Title')

# fails when the window name does not exist
fails(switch_to_window, window_name='not_a_window')

# fails when the window name does not exist
fails(switch_to_window, 'not_a_window')
