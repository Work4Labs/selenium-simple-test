from sst.actions import skip

skip('this test is skipped')
raise AssertionError('should never get here')
