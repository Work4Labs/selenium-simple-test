from sst.actions import *

# test get_page_source()

go_to('/')

txt = get_page_source()

assert (txt != '')
assert '<html' in txt
assert '</head>' in txt
assert '<body>' in txt
