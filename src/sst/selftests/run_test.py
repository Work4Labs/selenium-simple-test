from sst import actions
from sst.actions import *

foo = 3
args  = run_test('_test')
assert args == {
           'one': 'foo',
           'two': 2
        }

# check the context hasn't been altered
assert foo == 3

args = run_test('_test', one='ONE', two=3.1)
assert args == {
           'one': 'ONE',
           'two': 3.1
        }
