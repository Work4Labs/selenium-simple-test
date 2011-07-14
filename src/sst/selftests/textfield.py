from sst.actions import *


# password functionality is so close to textfield that
# we will include it with common textfield use


goto('/')

is_textfield('text_1')
is_textfield(get_element(id='text_1'))

is_textfield('pass_1')
is_textfield(get_element(id='pass_1'))

# fails for non existent element
fails(is_textfield, 'foobar')
# fails for element that exists but isn't a textfield
fails(is_textfield, 'radio_with_id_1')

textfield_write('text_1', "I pity the Foobar..")
text_is('text_1', "I pity the Foobar..")

textfield_write('text_1', "Overwriting")
text_is('text_1', "Overwriting")

textfield_write('text_1', "No checking", check=False)
text_is('text_1', "No checking")

# check with empty text
textfield_write('text_1', "")
text_is('text_1', "")

# checks the password field to see if it is editable
textfield_write('pass_1', "qaT3st")
text_is('pass_1', "qaT3st")
fails(text_is, 'pass_1', 'fake_text')

# fails for element that exists but is not editable
fails(textfield_write, 'text_2', "I pity the Foobar..")  # TODO: this line line is failing in Chrome
fails(text_is, 'text_2', "I pity the Foobar..")
