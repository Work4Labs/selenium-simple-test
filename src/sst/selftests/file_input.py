import os
from sst.actions import *

"""Test actions related to file input elements."""


goto('/')

# Assert that the input file is a textfield.
is_textfield('file_input')
is_textfield(get_element(id='file_input'))

# Enter a path to an existing file on the file input.
file_path = os.path.abspath(__file__)
textfield_write('file_input', file_path)
text_is('file_input', file_path)
