import os
from sst.actions import *

"""Test the assert_displayed action."""


go_to('/')

assert_displayed('select_with_id_1')
fails(assert_displayed, 'hidden_input')
