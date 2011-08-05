JAVASCRIPT_DISABLED = True

from sst.actions import *

goto('/nojs/')
text_is('test', "Before JS")

from sst import config
assert config.javascript_disabled
