from sst.actions import *

width, height = get_window_size()
assert isinstance(width, int)
assert isinstance(height, int)
assert width > 0
assert height > 0

set_window_size(400, 300)
width, height = get_window_size()
assert isinstance(width, int)
assert isinstance(height, int)
assert width == 400
assert height == 300

set_window_size(300, 400)
width, height = get_window_size()
assert isinstance(width, int)
assert isinstance(height, int)
assert width == 300
assert height == 400

