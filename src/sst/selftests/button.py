from sst.actions import *

go_to('/')

assert_button('mainform')
assert_button('lonely')
fails(assert_button, 'headline')
fails(assert_button, 'foobar')

assert_button(get_element(value='Begin', tag='input'))

# this button has no behaviour, but the action should not fail
click_button('lonely', wait=False)

# this button has no behaviour, but the action should not fail
click_button('lonely2', wait=False)

click_button('mainform')
assert_url('/begin')
assert_title('The Next Page')

click_link('the_band_link')
assert_url('/')

click_link('longscroll_link')
assert_url('/longscroll')

# button is initially scrolled out of view
click_button('mainform')
assert_url('/begin')