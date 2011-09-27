import os
from sst.actions import *

"""Test the is_displayed action."""


goto('/')

is_displayed('select_with_id_1')
fails(is_displayed, 'hidden_input')
