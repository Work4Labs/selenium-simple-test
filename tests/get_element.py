from funcrunner.actions import *

goto('/')

# need at least one parameter
fails(get_element)

elem = get_element(tag='title')
text_is(elem, "The Page Title")

# should fail if no elements match
fails(get_element, tag="foobar")

# should fail if more than one element found
fails(get_element, tag='p')

get_element(id='radio_with_id_1')
get_element(tag='input', id='radio_with_id_1')

fails(get_element, id="foobar")

get_element(css_class="unique_class")
get_element(css_class="unique_class", id="some_id")
get_element(css_class="unique_class", id="some_id", tag="p")
fails(get_element, css_class="some_class")
fails(get_element, css_class="foobar")

# checking arbitrary attributes
get_element(value="unique")
fails(get_element, value="first")

elem = get_element(type='radio', name='radio_with_id', checked="1")
is_radio(elem)
