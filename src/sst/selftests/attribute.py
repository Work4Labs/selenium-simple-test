from sst.actions import *

go_to('/')

assert_attribute('longscroll_link', 'name', 'longscroll')
assert_attribute('longscroll_link', 'name', 'scroll', regex=True)

fails(assert_attribute, 'longscroll_link', 'name', 'shortscroll')
fails(assert_attribute, 'longscroll_link', 'name', 'shortscroll', regex=True)
fails(assert_attribute, 'longscroll_link', 'fish', 'shortscroll')
fails(assert_attribute, 'longscroll_link', 'fish', 'shortscroll', regex=True)
