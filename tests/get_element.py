from funcrunner.actions import *

goto('/')

# need at least one parameter
fails(get_element)

elem = get_element(tag='title')
has_text(elem, "The Page Title")

# should fail if no elements match
fails(get_element, tag="foobar")

# should fail if more than one element found
fails(get_element, tag='p')
