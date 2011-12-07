from sst.actions import *


# password functionality is so close to textfield that
# we will include it with common textfield use


go_to('/')

assert_textfield('text_1')
assert_textfield(get_element(id='text_1'))

assert_textfield('pass_1')
assert_textfield(get_element(id='pass_1'))

# fails for non existent element
fails(assert_textfield, 'foobar')
# fails for element that exists but isn't a textfield
fails(assert_textfield, 'radio_with_id_1')

write_textfield('text_1', 'I pity the Foobar..')
assert_text('text_1', "I pity the Foobar..")

write_textfield('text_1', 'Overwriting')
assert_text('text_1', "Overwriting")

write_textfield('text_1', 'No checking', check=False)
assert_text('text_1', 'No checking')

# check with empty text
write_textfield('text_1', '')
assert_text('text_1', '')

# checks the password field to see if it is editable
write_textfield('pass_1', 'qaT3st')
assert_text('pass_1', 'qaT3st')
fails(assert_text, 'pass_1', 'fake_text')

