from funcrunner.actions import *

set_base_url('http://uec.pay/')
goto('/')

is_link(get_element(text='Log in'))
