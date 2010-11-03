from funcrunner.actions import *

goto('/')

is_textfield('text_1')
is_textfield(get_element(id='text_1'))

# fails for non existent element
fails(is_textfield, 'foobar')
# fails for element that exists but isn't a checkbox
fails(is_textfield, 'radio_with_id_1')

textfield_write('text_1',"I pity the Foobar..")
#fails for element that exists but is not editable
fails(textfield_write, 'text_2', "I pity the Foobar..")
