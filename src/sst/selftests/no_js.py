JAVASCRIPT_DISABLED = True

from sst.actions import *

go_to('/nojs/')
assert_text('test', "Before JS")

from sst import config
assert config.javascript_disabled
