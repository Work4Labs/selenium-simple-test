from funcrunner.actions import *

goto('/')

is_button('mainform')
fails(is_button, 'headline')
fails(is_button, 'foobar')
