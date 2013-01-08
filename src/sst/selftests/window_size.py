from sst.actions import *

width, height = get_window_size()
assert isinstance(width, int)
assert isinstance(height, int)
assert width > 0
assert height > 0

set_window_size(200, 300)
width, height = get_window_size()
assert isinstance(width, int)
assert isinstance(height, int)
assert width == 200
assert height == 300

expected_width, expected_height = set_window_size(500, 400)
width, height = get_window_size()
assert isinstance(width, int)
assert isinstance(height, int)
assert width == 500
assert height == 400
assert width == expected_width
assert height == expected_height

set_window_size(350, 350)
# set window to same size
set_window_size(350, 350)
width, height = get_window_size()
assert isinstance(width, int)
assert isinstance(height, int)
assert width == 350
assert height == 350
