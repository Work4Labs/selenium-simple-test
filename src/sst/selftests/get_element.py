from sst.actions import *

goto('/')
title_is('The Page Title')


# need at least one parameter
fails(get_element)

# simple title check
elem = get_element(tag='title')
text_is(elem, 'The Page Title')


# test attribute combos

elem = get_element(id='longscroll_link')
text_is(elem, 'Here is another link')

elem = get_element(tag='a', id='longscroll_link')
text_is(elem, 'Here is another link')

#elem = get_element(css_class='link class 1')  # failing!
#text_is(elem, 'Here is another link')

#elem = get_element(tag='a', css_class='link class 1')  # failing!
#text_is(elem, 'Here is another link')

#elem = get_element(tag='a', id='longscroll_link', css_class='link class 1')  # failing!
#text_is(elem, 'Here is another link')

elem = get_element(tag='a', id='longscroll_link', href='/longscroll')
text_is(elem, 'Here is another link')

elem = get_element(tag='a', id='longscroll_link', href='/longscroll', text='Here is another link')
text_is(elem, 'Here is another link')

elem = get_element(id='longscroll_link', href='/longscroll', text='Here is another link')
text_is(elem, 'Here is another link')

elem = get_element(href='/longscroll', text='Here is another link')
text_is(elem, 'Here is another link')

elem = get_element(href='/longscroll')
text_is(elem, 'Here is another link')



# should fail if no elements match
fails(get_element, tag='foobar')
fails(get_element, id='foobar')
fails(get_element, tag='foobar', id='foobar')

# should fail if more than one element found
fails(get_element, tag='p')

# radio buttons
elem = get_element(id='radio_with_id_1')
is_radio(elem)
elem = get_element(tag='input', id='radio_with_id_1')
is_radio(elem)
elem = get_element(type='radio', name='radio_with_id', checked='1')
is_radio(elem)

# find by css class
get_element(css_class='unique_class')
get_element(css_class='unique_class', id='some_id')
get_element(css_class='unique_class', id='some_id', tag='p')
fails(get_element, css_class='some_class')
fails(get_element, css_class="foobar")

# checking arbitrary attributes
get_element(value='unique')
fails(get_element, value='first')

# find by text
elem = get_element(tag='h2', text='Foo bar baz')
text_is(elem, 'Foo bar baz')
elem = get_element(text='Foo bar baz')
text_is(elem, 'Foo bar baz')

# find table row by text
get_element(tag='td', text='Get text from TD')

# should fail for a partial match
fails(get_element, text='Foo bar')
