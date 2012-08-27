from sst.actions import *

go_to('/')
url = get_current_url()
base_url = get_base_url()
assert_equal(base_url, 'http://localhost:8000/')
assert_equal(url, 'http://localhost:8000/')

go_to('/begin')
url = get_current_url()
base_url = get_base_url()
assert_equal(base_url, 'http://localhost:8000/')
assert_equal(url, 'http://localhost:8000/begin')
