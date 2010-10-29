from funcrunner.actions import *

goto('/')

url_is('/')
fails(url_is, '/foo')

title_is('The Page Title')
fails(title_is, 'this is not the title')
