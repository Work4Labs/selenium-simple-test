from sst.actions import *


goto('/')
link_click('popup_link')

# switch to new window/tab
switch_to_window(window_name='_NEW_WINDOW')
title_is('Popup Window')

# switch back to default/main window/tab
switch_to_window()
title_is('The Page Title')

# switch to new window/tab
switch_to_window(window_name='_NEW_WINDOW')
title_is('Popup Window')

# verify we can access content in new window
elem = get_element(tag='p', id='popup_id', text='Popup text here')
text_is(elem, 'Popup text here')

# switch back to default/main window/tab
switch_to_window(window_name='')
title_is('The Page Title')

# switch to new window/tab using index
switch_to_window(index=1)
title_is('Popup Window')

# switch back to default/main window using index
switch_to_window(index=0)
title_is('The Page Title')

# switch to new window/tab using name and index (index ignored when name works)
switch_to_window(window_name='_NEW_WINDOW', index=99)
title_is('Popup Window')

# switch back to default/main window
switch_to_window()
title_is('The Page Title')

# fails when the window name does not exist
fails(switch_to_window, window_name='not_a_window')

# fails when the window index does not exist
fails(switch_to_window, index=99)

# verify we are still back on main window
title_is('The Page Title')