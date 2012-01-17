from sst.actions import *

go_to('/tables')

assert_table_headers('empty', ['Head 0', 'Head 1', 'Head 2', 'Head 3'])
assert_table_has_rows('empty', 0)
assert_table_has_rows('one-row', 1)

fails(assert_table_headers, 'notthere',
      ['Head 0', 'Head 1', 'Head 2', 'Head 3'])
fails(assert_table_headers, 'empty', ['Head 0', 'Head 1', 'Head 2'])
fails(assert_table_headers, 'empty',
      ['Wrong', 'Head 1', 'Head 2', 'Head 3'])
fails(assert_table_has_rows, 'notthere', 0)
fails(assert_table_has_rows, 'empty', 1)

# XXXX Should this be able to work?
fails(assert_table_has_rows, 'no-body', 0)

fails(assert_table_has_rows, 'one-row', 0)
fails(assert_table_has_rows, 'one-row', 2)

assert_table_row_contains_text('one-row', 0,
    ['Cell 0', 'Cell 1', 'Cell 2', 'Cell 3'])
assert_table_row_contains_text('one-row', 0,
    ['Cell 0', 'Cell 1', 'Cell 2', 'Cell 3'], regex=True)
assert_table_row_contains_text('one-row', 0,
    ['^Cell', '^Cell', '^Cell', '^Cell'], regex=True)

fails(assert_table_row_contains_text, 'one-row', 0,
      ['Wrong', 'Cell 1', 'Cell 2', 'Cell 3'])
fails(assert_table_row_contains_text, 'one-row', 0,
      ['Cell 0', 'Cell 1', 'Cell 2'])
fails(assert_table_row_contains_text, 'one-row', 0,
      ['Cell 0', 'Cell 1', 'Cell 2', 'Extra'])
fails(assert_table_row_contains_text, 'one-row', 1, [])
fails(assert_table_row_contains_text, 'one-row', 0,
      ['Wrong', 'Cell 1', 'Cell 2', 'Cell 3'], regex=True)
fails(assert_table_row_contains_text, 'one-row', 0,
      ['Cell 0', 'Cell 1', 'Cell 2'], regex=True)
