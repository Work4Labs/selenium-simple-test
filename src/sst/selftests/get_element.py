from sst.actions import *


goto('/')
title_is('The Page Title')


# simple title check by tag
elem = get_element(tag='title')
text_is(elem, 'The Page Title')


# unique id
elem = get_element(id='longscroll_link')
text_is(elem, 'link to longscroll page')

# unique id + tag
elem = get_element(tag='a', id='longscroll_link')
text_is(elem, 'link to longscroll page')

# unique id + non-unique css_class
#elem = get_element(id='longscroll_link', css_class='link class 1')  # failing!
#text_is(elem, 'link to longscroll page')

# tag + unique id + non-unique css_class
#elem = get_element(tag='a', id='longscroll_link', css_class='link class 1')  # failing!
#text_is(elem, 'link to longscroll page')

# unique id + tag
elem = get_element(tag='a', id='longscroll_link')
text_is(elem, 'link to longscroll page')

# unique id + tag + href
elem = get_element(tag='a', id='longscroll_link', href='/longscroll')
text_is(elem, 'link to longscroll page')

# unique id + href
elem = get_element(id='longscroll_link', href='/longscroll')
text_is(elem, 'link to longscroll page')

# unique_id + tag + href + text
elem = get_element(tag='a', id='longscroll_link', href='/longscroll', text='link to longscroll page')
text_is(elem, 'link to longscroll page')

# unique_id + href + text
elem = get_element(id='longscroll_link', href='/longscroll', text='link to longscroll page')
text_is(elem, 'link to longscroll page')

# href + text
elem = get_element(href='/longscroll', text='link to longscroll page')
text_is(elem, 'link to longscroll page')

# href
elem = get_element(href='/longscroll')
text_is(elem, 'link to longscroll page')

# css_class
elem = get_element(css_class='unique_class')
text_is(elem, 'Some text here')

# css_class + unique_id
elem = get_element(css_class='unique_class', id='some_id')
text_is(elem, 'Some text here')

# css_class + unique_id + tag
elem = get_element(css_class='unique_class', id='some_id', tag='p')
text_is(elem, 'Some text here')

# arbitrary attribute
get_element(value='unique')

# text
elem = get_element(text='Foo bar baz')
text_is(elem, 'Foo bar baz')

# text + tag
elem = get_element(tag='h2', text='Foo bar baz')
text_is(elem, 'Foo bar baz')

# text + tag
elem = get_element(tag='td', text='Get text from TD')
text_is(elem, 'Get text from TD')


# radio buttons
elem = get_element(id='radio_with_id_1')
is_radio(elem)
elem = get_element(tag='input', id='radio_with_id_1')
is_radio(elem)
elem = get_element(type='radio', name='radio_with_id', checked='1')
is_radio(elem)


