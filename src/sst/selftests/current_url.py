from sst.actions import *

go_to('/')
url = get_current_url()
assert (url == 'http://localhost:8000/')

go_to('/begin')
url = get_current_url()
assert (url == 'http://localhost:8000/begin')

