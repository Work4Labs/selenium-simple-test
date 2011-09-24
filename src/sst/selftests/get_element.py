from sst.actions import *

goto('/')
title_is('The Page Title')


# simple title check
elem = get_element(tag='title')
text_is(elem, 'The Page Title')


# test attribute combos

elem = get_element(id='longscroll_link')
text_is(elem, 'link to longscroll page')

elem = get_element(tag='a', id='longscroll_link')
text_is(elem, 'link to longscroll page')

#elem = get_element(css_class='link class 1')  # failing!
#text_is(elem, 'link to longscroll page')

#elem = get_element(tag='a', css_class='link class 1')  # failing!
#text_is(elem, 'link to longscroll page')

#elem = get_element(tag='a', id='longscroll_link', css_class='link class 1')  # failing!
#text_is(elem, 'link to longscroll page')

elem = get_element(tag='a', id='longscroll_link', href='/longscroll')
text_is(elem, 'link to longscroll page')

elem = get_element(tag='a', id='longscroll_link', href='/longscroll', text='link to longscroll page')
text_is(elem, 'link to longscroll page')

elem = get_element(id='longscroll_link', href='/longscroll', text='link to longscroll page')
text_is(elem, 'link to longscroll page')

elem = get_element(href='/longscroll', text='link to longscroll page')
text_is(elem, 'link to longscroll page')

elem = get_element(href='/longscroll')
text_is(elem, 'link to longscroll page')


# find by css class
get_element(css_class='unique_class')
get_element(css_class='unique_class', id='some_id')
get_element(css_class='unique_class', id='some_id', tag='p')

# checking arbitrary attributes
get_element(value='unique')

# find by text
elem = get_element(tag='h2', text='Foo bar baz')
text_is(elem, 'Foo bar baz')
elem = get_element(text='Foo bar baz')
text_is(elem, 'Foo bar baz')

# find table row by text
elem = get_element(tag='td', text='Get text from TD')
text_is(elem, 'Get text from TD')

# radio buttons
elem = get_element(id='radio_with_id_1')
is_radio(elem)
elem = get_element(tag='input', id='radio_with_id_1')
is_radio(elem)
elem = get_element(type='radio', name='radio_with_id', checked='1')
is_radio(elem)


