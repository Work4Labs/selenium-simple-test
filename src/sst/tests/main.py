import testtools.run
import unittest2


class TestProgram(testtools.run.TestProgram):

    def __init__(self, module, argv, stdout=None, testRunner=None, exit=True):
        if testRunner is None:
            testRunner = unittest2.TextTestRunner
        super(TestProgram, self).__init__(module, argv=argv, stdout=stdout,
                                          testRunner=testRunner, exit=exit)


