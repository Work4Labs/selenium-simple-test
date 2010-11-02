from funcrunner.actions import *

goto('/')

is_link('the_band_link')
is_link(get_element(id='the_band_link'))

# fails for non existent element
fails(is_link, 'foobar')

# fails for element that exists but isn't a link
fails(is_link, 'radio_with_id_1')

#link_url_is('the_band_link', 'http://www.closingiris.com')
#link_url_is(get_element(id='the_band_link'), 'http://www.closingiris.com')
# fails when given the wrong value
#fails(link_url_is, 'the_band_link', 'http://www.notreal.com')

#link_text_is('the_band_link', 'Here is a link')
#link_text_is(get_element(id='the_band_link'), 'Here is a link')
#fails with the wrong value
#fails(link_text_is, 'the_band_link', 'Here is a link')

#link_follow('the_band_link')
#click and wait scenario
#404?
#No 'type' attribute to rely on
