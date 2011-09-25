from sst.actions import *


goto('/')
link_click('popup_link')

# switch to new window/tab
switch_to_window('_NEW_WINDOW')
title_is('Popup Window')

# fails when frame index is out of range
fails(switch_to_frame, index_or_name=2)

# switch to a valid frame index
switch_to_frame(index_or_name=1)
elem = get_element(id='frame_b_id')
text_is(elem, 'Frame B text here')

# fails because we are in sibling frame 
fails(get_element, id='frame_a_id')

# switch back to default frame
switch_to_frame()
get_element(tag='p', id='popup_id', text='Popup text here')
title_is('Popup Window')

# switch to a valid frame name
switch_to_frame(index_or_name='frame_a')
elem = get_element(id='frame_a_id')
text_is(elem, 'Frame A text here')

# switch back to default frame
switch_to_frame()
get_element(tag='p', id='popup_id', text='Popup text here')
title_is('Popup Window')

# switch back to default/main window/tab
switch_to_window()
title_is('The Page Title')



