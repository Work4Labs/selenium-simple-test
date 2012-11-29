#!/usr/bin/python

import sys
import unittest2

# Missing tests/features
# - discover 
# - list
# - start-with


# The tests we care about are all under src
sys.path.insert(0, './src')


class TestLoader(unittest2.TestLoader):
    """Custom TestLoader to extend the stock python one."""

    suiteClass = unittest2.TestSuite

    def loadTestsFromModuleNames(self, names):
        result = self.suiteClass()
        for name in names:
            result.addTests(self.loadTestsFromModuleName(name))
        return result

    def loadTestsFromModuleName(self, name):
        result = self.suiteClass()
        module = self._get_module_from_name(name)

        result.addTests(self.loadTestsFromModule(module))
        return result


class TestProgram(unittest2.TestProgram):

    def __init__(self, module='__main__'):
        # Tell unittest to call createTests
        unittest2.TestProgram.__init__(self, module, testLoader=TestLoader(),
                                       # Tell unittest to call createTests
                                       defaultTest=True,
                                       )

    def createTests(self):
        suite = self.testLoader.suiteClass()

        # In case we define tests in this file
        std_tests = self.testLoader.loadTestsFromModule(self.module)
        suite.addTests(std_tests)
        # Explicitly load tests from the listed modules
        other_tests = self.testLoader.loadTestsFromModuleNames([
                    'sst.tests.test_selftest',
                    ])
        suite.addTests(other_tests)
        self.test = suite


if __name__ == '__main__':
    TestProgram(module=__name__)
