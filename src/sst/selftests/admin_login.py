from sst.actions import *

import helpers


# skip this test when running from CI
helpers.skip_as_jenkins()

go_to('/admin/')
assert_title_contains('Django site admin')

# logout of Admin if needed
elem = get_element(tag='title')
if 'Log in' not in elem.text:
    click_link(get_element(text='Log out'))
    assert_title('Logged out | Django site admin')
    refresh()

assert_title('Log in | Django site admin')

# login to Admin site
write_textfield('id_username', 'sst')
write_textfield('id_password', 'password')
click_element(get_element(value='Log in'))
assert_title('Site administration | Django site admin')
assert_element(tag='h1', id='site-name', text='Django administration')

# make sure you didn't get bounced back to login page
fails(assert_title, 'Log in | Django site admin')

# logout
click_link(get_element(text='Log out'))
assert_title('Logged out | Django site admin')
