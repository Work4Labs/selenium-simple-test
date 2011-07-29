JAVASCRIPT_DISABLED = True

from sst.actions import *

goto('/nojs/')
text_is('test', "Before JS")
