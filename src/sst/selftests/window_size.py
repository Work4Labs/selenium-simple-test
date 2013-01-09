from sst.actions import *


width, height = get_window_size()
assert isinstance(width, int)
assert isinstance(height, int)
assert width > 0
assert height > 0

expected_width, expected_height = set_window_size(200, 300)
width, height = get_window_size()
assert isinstance(expected_width, int)
assert isinstance(expected_height, int)
assert width == expected_width == 200
assert height == expected_height == 300

expected_width, expected_height = set_window_size(450, 420)
width, height = get_window_size()
assert width == expected_width == 450
assert height == expected_height == 420

expected_width, expected_height = set_window_size(380, 320)
# set window to same size
set_window_size(380, 320)
width, height = get_window_size()
assert width == expected_width == 380
assert height == expected_height == 320

go_to('/')

# switch to new window/tab and resize it
click_link('popup_link')
switch_to_window(index_or_name='_NEW_WINDOW')
assert_title('Popup Window')
expected_width, expected_height = set_window_size(260, 275)
width, height = get_window_size()
assert width == expected_width == 260
assert height == expected_height == 275
