from sst.actions import *

go_to('/html5')

assert_textfield('email')
write_textfield('email', 'foo@bar.com', check=True)

assert_textfield('url')
write_textfield('url', 'http://localhost:8000', check=True)

assert_textfield('search')
write_textfield('search', 'something', check=True)

assert_textfield('number')
write_textfield('number', '33', check=True)
