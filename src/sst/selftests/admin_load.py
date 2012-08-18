from sst.actions import *

import helpers


# skip this test when running from CI
helpers.skip_as_jenkins()

go_to('/admin/')
assert_title('Log in | Django site admin')
