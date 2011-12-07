import os
from sst.actions import *

"""Test actions related to file input elements."""


go_to('/')

# Assert that the input file is a textfield.
assert_textfield('file_input')
assert_textfield(get_element(id='file_input'))

# Enter a path to an existing file on the file input.
file_path = os.path.abspath(__file__)
write_textfield('file_input', file_path)
assert_text('file_input', file_path)
