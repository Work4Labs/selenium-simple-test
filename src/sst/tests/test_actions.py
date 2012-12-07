from cStringIO import StringIO
import sys


import testtools


from sst import actions


class TestRetryOnStale(testtools.TestCase):

    def test_retry_on_stale_only_once(self):
        """retry once on StaleElementReferenceException."""
        self.nb_calls = 0

        @actions.retry_on_stale_element
        def raiser():
            self.nb_calls += 1
            if self.nb_calls == 1:
                raise actions.StaleElementReferenceException('whatever')
            return 'success'

        out = StringIO()
        self.patch(sys, 'stdout', out)
        # Calling the function succeeds
        self.assertEqual('success', raiser())
        # But under the hood it's been called twice
        self.assertEqual(2, self.nb_calls)
        # And we get some feedback about the exception
        self.assertEqual(
            '    Retrying after catching: StaleElementReferenceException()\n',
            out.getvalue())

    def test_wait_for_retries(self):
        self.nb_calls = 0

        def raiser():
            self.nb_calls += 1
            if self.nb_calls == 1:
                raise actions.StaleElementReferenceException('whatever')
            return True

        out = StringIO()
        self.patch(sys, 'stdout', out)
        # Calling the function succeeds
        self.assertEqual(None, actions.wait_for(raiser))
        # But under the hood it's been called twice
        self.assertEqual(2, self.nb_calls)
        # And we get some feedback about the exception
        self.assertEqual('''\
    Waiting for 'raiser'
    Retrying after catching: StaleElementReferenceException()
    Waiting for 'raiser'
''',
            out.getvalue())

