from sst.actions import *

goto('/')

is_button('mainform')
is_button('lonely')
fails(is_button, 'headline')
fails(is_button, 'foobar')

is_button(get_element(value="Begin", tag="input"))

# this button has no behaviour, but the action should not fail
button_click('lonely', wait=False)

button_click('mainform')
url_is('/begin')
title_is('The Next Page')

link_click('the_band_link')
url_is('/')

link_click('longscroll_link')
url_is('/longscroll')

# button is initially scrolled out of view
button_click('mainform')
url_is('/begin')