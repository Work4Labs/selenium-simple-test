from sst.actions import *

assert_equal(1, 1)
assert_equal('foo', 'foo')

fails(assert_equal, 1, 2)
fails(assert_equal, 'foo', 'bar')

assert_not_equal(1, 2)
assert_not_equal('foo', 'bar')

fails(assert_not_equal, 1, 1)
fails(assert_not_equal, 'foo', 'foo')
