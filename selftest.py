#!/usr/bin/python

import sys


import testtools
from testtools import run as tt_run


# Missing tests/features
# - start-with

class TestProgram(tt_run.TestProgram):

    def __init__(self, module, argv):
        super(TestProgram, self).__init__(module, argv=argv)


if __name__ == '__main__':
    # We discover tests under src/sst/tests, the python 'load_test' protocol
    # can be used in test modules for more fancy stuff.
    discover_args = ['discover', '-s', './src/sst/tests', '-t', './src']
    TestProgram(__name__, argv=[sys.argv[0]] + discover_args + sys.argv[1:])
