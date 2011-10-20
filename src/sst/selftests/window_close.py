from sst.actions import *

goto('/')
link_click('popup_link')

# switch to new window/tab and close it
switch_to_window(index_or_name='_NEW_WINDOW')
title_is('Popup Window')
window_close()

# switch back to default/main window/tab
switch_to_window()
title_is('The Page Title')

# fails because the window no longer exists
fails(switch_to_window, index_or_name='NEW_WINDOW')
