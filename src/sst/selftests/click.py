from sst.actions import *

go_to('/')

# checks that clicking works at the element level as well
click_element(get_element(id='the_band_link'), wait=False)
assert_url('/begin')

go_to('/')

# checks the wait option 
click_element(get_element(id='the_band_link'), wait=True)
assert_url('/begin')
