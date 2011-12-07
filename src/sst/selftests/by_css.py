from sst.actions import *

go_to('/')

get_element_by_css('#headline')
get_element_by_css('.unique_class')

fails(get_element_by_css, '#doesnotexist')
fails(get_element_by_css, '.someclass')

assert len(get_elements_by_css('#doesnotexist')) == 0
assert len(get_elements_by_css('#headline')) == 1
assert len(get_elements_by_css('.some_class')) == 2
