from sst.actions import *


before_width = 300
before_height = 200

go_to('/')

# reset size
set_window_size(before_width, before_height)

go_to('/')

# maximize main window
maximize_window()
width, height = get_window_size()
assert width > before_width 
assert height > before_height

go_to('/')

# re-maximize window
maximize_window()
width, height = get_window_size()
assert width > before_width 
assert height > before_height

go_to('/')

# reset size
set_window_size(before_width, before_height)
width, height = get_window_size()
assert width == before_width
assert height == height

go_to('/')

# switch to new window/tab and maximize it
click_link('popup_link')
switch_to_window(index_or_name='_NEW_WINDOW')
assert_title('Popup Window')
maximize_window()
width, height = get_window_size()
assert width > before_width 
assert height > before_height
