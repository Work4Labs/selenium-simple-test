goto('/')

# checks that clicking works at the element level as well
element_click(get_element(id='the_band_link'), wait=False)
url_is('/begin')

