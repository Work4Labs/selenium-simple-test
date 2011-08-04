from sst import actions
from sst.actions import *

# tests goto, url_is, title_is, set_base_url
# reset_base_url

goto('/')

url_is('/')
fails(url_is, '/foo')

title_is('The Page Title')
fails(title_is, 'this is not the title')

title_contains('The Page')
title_contains('.*Pag[E|e]', regex=True)
fails(title_contains, 'foobar')

set_base_url('localhost:8000')
assert actions.BASE_URL == 'http://localhost:8000/'

set_base_url('http://localhost:8000/begin/')
goto('/')

# url_is adds the base url for relative urls
# so test both ways
url_is('http://localhost:8000/begin/')
url_is('/')

fails(url_is, 'http://localhost:8000/')
fails(url_is, '/begin/')

reset_base_url()
goto('/')
url_is('http://localhost:8000/')
