from sst.actions import *


set_wait_timeout(10)
assert get_wait_timeout() == 10

set_wait_timeout(20)
assert get_wait_timeout() == 20
