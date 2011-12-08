from sst.actions import *

go_to('/')

assert exists_element(id='select_with_id_1')
assert not exists_element(id='non_existing_element')
