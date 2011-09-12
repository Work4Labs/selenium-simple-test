from sst.actions import *

goto('/')

# checks that clicking works at the element level as well
element_click(get_element(id='the_band_link'), wait=False)
url_is('/begin')

goto('/')

# checks the wait option 
element_click(get_element(id='the_band_link'), wait=True)
url_is('/begin')
