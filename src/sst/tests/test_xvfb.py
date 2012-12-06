import os


import testtools


from sst import xvfbdisplay


class TestXvfb(testtools.TestCase):

    def test_start(self):
        xvfb = xvfbdisplay.Xvfb()
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(':%d' % xvfb.vdisplay_num, os.environ['DISPLAY'])
        self.assertIsNot(None, xvfb.xvfb_proc)

    def test_stop(self):
        orig = os.environ['DISPLAY']
        xvfb = xvfbdisplay.Xvfb()
        xvfb.start()
        self.assertNotEqual(orig, os.environ['DISPLAY'])
        xvfb.stop()
        self.assertEquals(orig, os.environ['DISPLAY'])
