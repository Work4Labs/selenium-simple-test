from sst.actions import *

""" negative (fails) tests for object identification """


go_to('/')
assert_title('The Page Title')


# need at least one parameter
fails(get_element)

# should fail if no elements match
fails(get_element, tag='foobar')
fails(get_element, id='foobar')
fails(get_element, tag='foobar', id='foobar')

# should fail if more than one element found
fails(get_element, tag='p')

# find by css class
fails(get_element, css_class='some_class')
fails(get_element, css_class="foobar")

# checking arbitrary attributes
fails(get_element, value='first')

# should fail for a partial match
fails(get_element, text='Foo bar')
