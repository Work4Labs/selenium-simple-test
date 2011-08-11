from sst.actions import *


goto('/')

u = 'שאלק'
textfield_write('text_1', u)
text_is('text_1', u)

u = u'abcdéשאלק'
textfield_write('text_1', u)
text_is('text_1', u)

u =  u'\u05e9\u05d0\u05dc\u05e7'
textfield_write('text_1', u)
text_is('text_1', u)

u = unichr(40960) + u'abcd' + unichr(1972)
textfield_write('text_1', u)
text_is('text_1', u)

