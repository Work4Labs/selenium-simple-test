from sst.actions import *

goto('/')

is_link('the_band_link')
is_link(get_element(id='the_band_link'))

# fails for non existent element
fails(is_link, 'foobar')

# fails for element that exists but isn't a link
fails(is_link, 'radio_with_id_1')

link_click('the_band_link')
