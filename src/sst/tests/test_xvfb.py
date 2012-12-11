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


class Headless(runtests.SSTTestCase):
    """A specialized test class for tests around xvfb."""

    xserver_headless = True

    # We don't use a browser here so disable its use to speed the tests
    # (i.e. the browser won't be started)
    def start_browser(self):
        pass

    def stop_browser(self):
        pass


class TestSSTTestCaseWithXfvb(testtools.TestCase):

    def setUp(self):
        super(TestSSTTestCaseWithXfvb, self).setUp()
        # capture test output so we don't pollute the test runs
        self.out = StringIO()
        self.patch(sys, 'stdout', self.out)

    def assertRunSuccessfully(self, test):
        result = testtools.TestResult()
        test.run(result)
        self.assertEqual([], result.errors)
        self.assertEqual([], result.failures)

    def test_headless_new_xvfb(self):
        class HeadlessNewXvfb(Headless):

            def test_headless(self):
                # A headless server has been started for us
                self.assertNotEqual(None, self.xvfb.xvfb.proc)

        self.assertRunSuccessfully(HeadlessNewXvfb("test_headless"))

    def test_headless_reused_xvfb(self):
        external_xvfb = xvfbdisplay.Xvfb()
        external_xvfb.start()
        self.addCleanup(external_xvfb.stop)

        class HeadlessReusedXvfb(Headless):

            xvfb = runtests.XvfbFixture(external_xvfb)

            def test_headless(self):
                # We reuse the existing xvfb
                self.assertIs(external_xvfb, self.xvfb.xvfb)

        self.assertRunSuccessfully(HeadlessReusedXvfb("test_headless"))
