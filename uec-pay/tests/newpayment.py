from funcrunner.actions import *

# passwords.py must exist in the uec-pay directory
from passwords import username, password

set_base_url('https://staging.pay.ubuntu.com/')
goto('/')
link_click(get_element(text='Log in'))

url_contains('https://login.staging.launchpad.net/')
textfield_write('id_email', username)
textfield_write('id_password', password)
button_click(get_element(css_class='btn', name='continue'))
url_is('https://staging.pay.ubuntu.com/payment/')

# testconsumer
goto('/test/')
link_click(get_element(text='Click here'))
sleep(20)
