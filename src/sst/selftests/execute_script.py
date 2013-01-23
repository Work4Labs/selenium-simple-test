from sst.actions import *


go_to('/')


orig_title = 'The Page Title'
new_title = 'New Title'


# get original title.
assert_title(orig_title)
orig_elem = get_element(tag='title')

# change the title with javascript.
script = 'document.title = "%s"' % new_title
execute_script(script)

# check title was changed.
assert_title(new_title)
assert_not_equal(orig_elem, get_element(tag='title'))

# refresh title is changed back after refresh.
refresh()
assert_title(orig_title)

# check the return value of the script.
assert execute_script('return 5') == 5
