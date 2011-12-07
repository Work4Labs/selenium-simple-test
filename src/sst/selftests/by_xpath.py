from sst.actions import *

# xpath locator tests
#
# see: http://seleniumhq.org/docs/appendix_locating_techniques.html 

go_to('/')

get_element_by_xpath("//p[contains(@class, 'unique_class')]")
get_element_by_xpath("//a[contains(@id, 'band_link')]")
get_element_by_xpath("//a[starts-with(@id, 'the_band_l')]")

get_elements_by_xpath('//p')
get_elements_by_xpath("//p[contains(@class, 'some_class')]")

fails(get_element_by_xpath, '//doesnotexist')
fails(get_element_by_xpath, "//a[contains(@id, 'doesnotexist')]")

assert len(get_elements_by_xpath('//doesnotexist')) == 0
assert len(get_elements_by_xpath("//p[contains(@class, 'unique_class')]")) == 1
assert len(get_elements_by_xpath("//p[contains(@class, 'some_class')]")) == 2
