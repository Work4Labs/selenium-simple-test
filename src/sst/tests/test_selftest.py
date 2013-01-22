from cStringIO import StringIO


import testtools


# The following two imports are required by unittest when running a list of
# test names like test_list_single does below (that's probably a bug in
# TestLoader.loadTestsFromName...) -- vila 2012-11-29
import sst
import sst.tests
from sst.tests import main


class TestTestProgram(testtools.TestCase):

    def run_test_program(self, argv, out):
        main.TestProgram(__name__, argv=['dummy'] + argv, stdout=out,
                         exit=False)

    def test_list(self):
        out = StringIO()
        self.run_test_program(['-l'], out)
        # At least this test should appear in the list (we don't check for an
        # exact list or this test will fail each time a new one is added).
        self.assertIn(self.id(), out.getvalue())

    def test_list_single(self):
        out = StringIO()
        self.run_test_program(['-l', self.id()], out)
        self.assertEqual(self.id() + '\n', out.getvalue())
