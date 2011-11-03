from sst.actions import *

goto('/')
url = get_current_url()
assert (url == 'http://localhost:8000/')

goto('/begin')
url = get_current_url()
assert (url == 'http://localhost:8000/begin')
