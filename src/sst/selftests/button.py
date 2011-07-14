from sst.actions import *

goto('/')

is_button('mainform')
fails(is_button, 'headline')
fails(is_button, 'foobar')

is_button(get_element(value="Begin", tag="input"))

button_click('mainform')
url_is('/begin')
title_is('The Next Page')
