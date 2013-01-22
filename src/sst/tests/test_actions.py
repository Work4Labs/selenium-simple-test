from cStringIO import StringIO
import sys


import testtools


from sst import actions


class TestRetryOnStale(testtools.TestCase):

    def setUp(self):
        super(TestRetryOnStale, self).setUp()
        self.out = StringIO()
        # Capture output from retry_on_stale_element calls
        self.patch(sys, 'stdout', self.out)
        self.nb_calls = 0

    def raise_stale_element(self):
        self.nb_calls += 1
        if self.nb_calls == 1:
            raise actions.StaleElementReferenceException('whatever')
        return 'success'

    def assertRaisesOnlyOnce(self, expected, func, *args):
        # Calling the function succeeds
        self.assertEqual(expected, func(*args))
        # But under the hood it's been called twice
        self.assertEqual(2, self.nb_calls)
        # And we get some feedback about the exception
        self.assertIn(
            '    Retrying after catching: StaleElementReferenceException()\n',
            self.out.getvalue())

    def test_retry_on_stale_only_once(self):
        """retry once on StaleElementReferenceException."""
        @actions.retry_on_stale_element
        def protected_raiser():
            return self.raise_stale_element()

        self.assertRaisesOnlyOnce('success', protected_raiser)

    def test_wait_for_retries(self):
        self.assertRaisesOnlyOnce(None, actions.wait_for,
                                  self.raise_stale_element)
