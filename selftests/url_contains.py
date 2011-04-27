from funcrunner.actions import *

goto('/')

url_contains('http://localhost:8000')
url_contains('localhost')
fails(url_contains, 'foobar')
