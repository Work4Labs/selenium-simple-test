"""Test the assert_displayed action."""

from sst.actions import *


go_to('/')

assert_displayed('select_with_id_1')
fails(assert_displayed, 'hidden_input')
