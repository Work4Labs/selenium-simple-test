from sst.actions import *

go_to('/')

assert_url_contains('http://localhost:8000')
assert_url_contains('localhost')
assert_url_contains('lo[C|c]a.*host', regex=True)
fails(assert_url_contains, 'foobar')
