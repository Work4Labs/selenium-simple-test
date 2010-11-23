from funcrunner.actions import *

set_base_url('http://uec.pay/')
goto('/')

is_link(get_element(text='Log in'))
link_click(get_element(text='Log in'))

url_contains('https://login.staging.launchpad.net/')