from sst.actions import *

goto('/')

# need at least one parameter
fails(get_element)

# simple title check
elem = get_element(tag='title')
text_is(elem, 'The Page Title')

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

# find table row
get_element(tag='td', text='Get text from TD')

# should fail for a partial match
fails(get_element, text='Foo bar')
