import os
from sst.actions import *

"""Test the element_is_displayed action."""


goto('/')

element_is_displayed('select_with_id_1')
fails(element_is_displayed, 'hidden_input')
