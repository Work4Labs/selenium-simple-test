from sst.actions import *


go_to('/')

before_width = 300
before_height = 200

# maximize main window
set_window_size(before_width, before_height)
maximize_window()
width, height = get_window_size()
assert width > before_width 
assert height > before_height

# switch to new window/tab and maximize it
click_link('popup_link')
switch_to_window(index_or_name='_NEW_WINDOW')
assert_title('Popup Window')
set_window_size(before_width, before_height)
maximize_window()
width, height = get_window_size()
assert width > before_width 
assert height > before_height
