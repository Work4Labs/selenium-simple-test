import os
import sys
from cStringIO import StringIO


import testtools


from sst import (
    runtests,
    xvfbdisplay,
)
from sst.tests import main

class TestXvfb(testtools.TestCase):

    def test_start(self):
        xvfb = xvfbdisplay.Xvfb()
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(':%d' % xvfb.vdisplay_num, os.environ['DISPLAY'])
        self.assertIsNot(None, xvfb.proc)

    def test_stop(self):
        orig = os.environ['DISPLAY']
        xvfb = xvfbdisplay.Xvfb()
        xvfb.start()
        self.assertNotEqual(orig, os.environ['DISPLAY'])
        xvfb.stop()
        self.assertEquals(orig, os.environ['DISPLAY'])


class TestSSTTestCaseWithXfvb(testtools.TestCase):

    def setUp(self):
        super(TestSSTTestCaseWithXfvb, self).setUp()
        # capture test output so we don't pollute the test runs
        self.out = StringIO()
        self.patch(sys, 'stdout', self.out)

    def test_headless_new_xvfb(self):
        class Headless(runtests.SSTTestCase):

            xserver_headless = True

            def test_headless(self):
                # A headless server has been started for us
                self.assertNotEqual(None, self.xvfb.proc)

        test = Headless("test_headless")
        result = testtools.TestResult()
        test.run(result)
        self.assertEqual([], result.errors)
        self.assertEqual([], result.failures)

    def test_headless_reused_xvfb(self):
        external_xvfb = xvfbdisplay.Xvfb()
        external_xvfb.start()
        self.addCleanup(external_xvfb.stop)

        class Headless(runtests.SSTTestCase):

            xserver_headless = True
            xvfb = external_xvfb

            def test_headless(self):
                # We reuse the existing xvfb
                self.assertIs(external_xvfb, self.xvfb)

        test = Headless("test_headless")
        result = testtools.TestResult()
        test.run(result)
        self.assertEqual([], result.errors)
        self.assertEqual([], result.failures)
