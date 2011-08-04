from sst.actions import *

goto('/')

url_contains('http://localhost:8000')
url_contains('localhost')
url_contains('lo[C|c]a.*host', regex=True)
fails(url_contains, 'foobar')
