from sst.actions import *

goto('/html5')

is_textfield('email')
textfield_write('email', 'foo@bar.com', check=True)

is_textfield('url')
textfield_write('url', 'http://localhost:8000', check=True)

is_textfield('search')
textfield_write('search', 'something', check=True)

is_textfield('number')
textfield_write('number', '33', check=True)
