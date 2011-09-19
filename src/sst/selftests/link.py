from sst.actions import *

goto('/')

is_link('the_band_link')
is_link(get_element(id='the_band_link'))

# fails for non existent element
fails(is_link, 'foobar')

# fails for element that exists but isn't a link
fails(is_link, 'radio_with_id_1')


link_click('the_band_link', wait=False)
url_is('/begin')

link_click('the_band_link')
url_is('/')

link_click('longscroll_link')
url_is('/longscroll')

link_click('homepage_link_top')
url_is('/')

link_click('longscroll_link')
url_is('/longscroll')

# link is initially scrolled out of view
link_click('homepage_link_bottom') 
url_is('/')
