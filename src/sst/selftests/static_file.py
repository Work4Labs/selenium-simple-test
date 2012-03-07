
# test for loading local files by file:// rather than http://

import os

from sst.actions import *


static_file = os.path.join(''.join(os.path.split(__file__)[:-1]), 'static.html')

# using full path
go_to('file:////%s' % static_file)
assert_title('The Static Page')
assert_element(tag='h1', text='Hello World')

# using base_url
set_base_url('file:////')
go_to(static_file)
assert_title('The Static Page')
assert_element(tag='h1', text='Hello World')
