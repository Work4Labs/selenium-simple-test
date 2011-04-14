from funcrunner.actions import *

goto('/')

elem = get_element(tag='td', text='Get text from TD')
print elem.text

