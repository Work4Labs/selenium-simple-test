from cStringIO import StringIO
import sys


import testtools


from sst import actions


class TestRetryOnStale(testtools.TestCase):

    def test_retry_on_stale_only_once(self):
        """retry once on StaleElementReferenceException."""
        self.nb_calls = 0

        def raiser():
            self.nb_calls += 1
            if self.nb_calls == 1:
                raise actions.StaleElementReferenceException('whatever')
            return 'success'

        out = StringIO()
        self.patch(sys, 'stdout', out)
        self.assertEqual('success', actions.retry_on_stale_element(raiser)())
        self.assertEqual(2, self.nb_calls)
        self.assertEqual(
            '    Retrying after catching: StaleElementReferenceException()\n',
            out.getvalue())

