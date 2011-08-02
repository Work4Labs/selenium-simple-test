from sst.actions import *

set_wait_timeout(6, 0.3)
set_base_url('http://bar/')

args = {}

foo = 6
args['one'] = get_argument('one', 'foo')
args['two'] = get_argument('two', 2)

RESULT = args
