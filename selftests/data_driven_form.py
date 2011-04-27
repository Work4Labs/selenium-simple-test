from funcrunner.actions import *


# vars from data_driven_form.csv are available in namespace
assert('textfield1' in dir())
assert('password1' in dir())
    

goto('/')
title_is('The Page Title')

textfield_write(get_element(name='textfield1'), textfield1) # textfield1 comes from the associated csv data file
textfield_write(get_element(name='password1'), password1)
button_click(get_element(tag='input', value='Begin'))
title_is('The Next Page')
