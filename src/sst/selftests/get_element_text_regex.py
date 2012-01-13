from sst.actions import *

go_to('/')


num_links = len(get_elements(tag='a'))

assert num_links == len(get_elements(tag='a', text_regex='.*'))


get_element(tag='p', text_regex='^Some text here')
exists_element(tag='p', text_regex='^Some text here')

get_element(tag='p', text_regex='^Some text.*$')
exists_element(tag='p', text_regex='^Some text.*$')

assert len(get_elements(tag='p', text_regex='^Some text.*$')) == 1

