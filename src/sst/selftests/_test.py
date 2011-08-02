from sst.actions import *

args = {}

foo = 6
args['one'] = get_argument('one', 'foo')
args['two'] = get_argument('two', 2)

RESULT = args
