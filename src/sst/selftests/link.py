from sst.actions import *

go_to('/')

assert_link('the_band_link')
assert_link(get_element(id='the_band_link'))

# fails for non existent element
fails(assert_link, 'foobar')

# fails for element that exists but isn't a link
fails(assert_link, 'radio_with_id_1')


click_link('the_band_link', wait=False)
assert_url('/begin')

click_link('the_band_link')
assert_url('/')

click_link('longscroll_link')
assert_url('/longscroll')

click_link('homepage_link_top')
assert_url('/')

click_link('longscroll_link')
assert_url('/longscroll')

# link is initially scrolled out of view
click_link('homepage_link_bottom') 
assert_url('/')
