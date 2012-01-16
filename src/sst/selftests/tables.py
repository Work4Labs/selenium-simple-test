from sst.actions import *

go_to('/tables')

assert_table_headers('empty', ['Head 0', 'Head 1', 'Head 2', 'Head 3'])
assert_table_has_rows('empty', 0)

fails(assert_table_headers, 'notthere',
      ['Head 0', 'Head 1', 'Head 2', 'Head 3'])
fails(assert_table_headers, 'empty', ['Head 0', 'Head 1', 'Head 2'])
fails(assert_table_headers, 'empty',
      ['Wrong', 'Head 1', 'Head 2', 'Head 3'])
fails(assert_table_has_rows, 'notthere', 0)
fails(assert_table_has_rows, 'empty', 1)

