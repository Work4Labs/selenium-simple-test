from funcrunner.actions import *
from _actions import login

login()

# testconsumer
goto('/test/')
link_click(get_element(text='Click here'))
sleep(20)
