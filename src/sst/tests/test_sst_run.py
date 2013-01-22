import testtools

from sst import runtests


class TestSSTScriptTestCase(testtools.TestCase):

    def test_id(self):
        """The test id mentions the python class path and the test name."""
        # FIXME: This is a minimal test to cover http://pad.lv/1087606, it
        # would be better to check a results.xml file but we don't have the
        # test infrastructure for that (yet) -- vila 2012-12-07
        test = runtests.SSTScriptTestCase('foo')
        self.assertEqual('sst.runtests.SSTScriptTestCase.foo', test.id())
