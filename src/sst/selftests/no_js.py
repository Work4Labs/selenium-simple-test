JAVASCRIPT_DISABLED = True

from sst.actions import *

goto('/nojs/')
waitfor(title_is, "No JavaScript Test")
text_is('test', "Before JS")
