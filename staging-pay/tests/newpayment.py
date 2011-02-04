from funcrunner.actions import *
from _actions import login

# login to payments
login()

# testconsumer
goto('/test/')

get_element(tag='h2', text='Welcome to the Test Consumer!')
get_element(tag='h2', text='Create a new payment')

link_click(get_element(text='Click here'))
url_is('/test/new/')

get_element(tag='h2', text='New payment')

item_description="""A funky foobar
With several lines of description
like this"""
textfield_write('1-item_description', item_description)
