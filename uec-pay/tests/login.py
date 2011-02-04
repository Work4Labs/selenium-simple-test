from funcrunner.actions import *

# passwords.py must exist in the staging-pay directory
from passwords import username, password

set_base_url('https://staging.pay.ubuntu.com/')
goto('/')

is_link(get_element(text='Log in'))
link_click(get_element(text='Log in'))

url_contains('https://login.staging.launchpad.net/')

get_element(tag='h2', text='Sign in to Staging Payments Service')
is_textfield('id_email')
is_textfield('id_password')
textfield_write('id_email', username)
textfield_write('id_password', password)

button_click(get_element(css_class='btn', name='continue'))
url_is('https://staging.pay.ubuntu.com/payment/')

# main page
get_element(tag='h1', text="Your payment history")
