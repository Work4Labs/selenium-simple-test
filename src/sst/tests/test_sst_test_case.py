#   Copyright (c) 2013 Canonical Ltd.
#
#   This file is part of: SST (selenium-simple-test)
#   https://launchpad.net/selenium-simple-test
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import cStringIO
import os

import mock
import testtools

from sst import tests


class TestResultsDirectory(testtools.TestCase):

    def setUp(self):
        super(TestResultsDirectory, self).setUp()
        tests.set_cwd_to_tmp(self)

    def test_results_directory_is_created(self):

        class WithResultsDir(tests.SSTBrowserLessTestCase):

            results_directory = 'results'

            def test_pass_and_leaves_a_results_dir(self):
                pass

        test = WithResultsDir('test_pass_and_leaves_a_results_dir')
        result = testtools.TestResult()
        test.run(result)
        # FIXME: The following assertion outlines that config.results_directory
        # is modified as a side-effect, this violates isolation.
        # -- vila 2013-01-15
        from sst import config
        self.assertTrue(os.path.exists(config.results_directory))
        self.assertTrue(os.path.exists('results'))


class TestHandleExceptions(testtools.TestCase):

    def setUp(self):
        super(TestHandleExceptions, self).setUp()
        tests.set_cwd_to_tmp(self)
        self.result = testtools.TestResult()

    def get_handle_exceptions_test(self, with_screenshots=False,
                                   with_debug_post_mortem=False,
                                   with_extended_report=False):
        class ForHandleExceptionsTests(tests.SSTBrowserLessTestCase):

            screenshot_calls = 0
            screenshots_on = with_screenshots
            debug_post_mortem = with_debug_post_mortem
            extended_report = with_extended_report

            def take_screenshot_and_page_dump(self):
                """Counts the calls.

                We don't have a browser so won't be able to do a real
                screenshot anyway.
                """
                self.screenshot_calls += 1

            def test_it(self):
                """An always failing test."""
                self.assertTrue(False)

        return ForHandleExceptionsTests('test_it')

    def test_screenshot_and_page_dump_on_failure_enabled(self):
        test = self.get_handle_exceptions_test(with_screenshots=True)
        test.run()
        self.assertEquals(1, test.screenshot_calls)

    def test_screenshot_and_page_dump_on_failure_disabled(self):
        test = self.get_handle_exceptions_test(with_screenshots=False)
        test.run()
        self.assertEquals(0, test.screenshot_calls)

    @mock.patch('pdb.post_mortem')
    @mock.patch('sys.stderr', new_callable=cStringIO.StringIO)
    def test_debug_post_mortem_enabled(self, mock_stderr, mock_post_mortem):
        test = self.get_handle_exceptions_test(with_debug_post_mortem=True)
        test.run()
        self.assertTrue(mock_stderr.getvalue().endswith,
                        'AssertionError: False is not true')
        mock_post_mortem.assert_called_with()

    def test_debug_post_mortem_disabled(self):
        test = self.get_handle_exceptions_test(with_debug_post_mortem=False)
        with mock.patch.object(test, 'print_exception_and_enter_post_mortem'):
            test.run()
            self.assertFalse(test.print_exception_and_enter_post_mortem.called)

    def test_report_extensively_enabled(self):
        test = self.get_handle_exceptions_test(with_extended_report=True)
        with mock.patch.object(test, 'addDetail'):
            test.run()
            test.addDetail.assert_called_with(
                'Original exception: AssertionError: False is not true\n\n'
                'Current url: unavailable\n\nPage source:\n\nunavailable\n\n')

    def test_report_extensively_disabled(self):
        test = self.get_handle_exceptions_test(with_extended_report=False)
        with mock.patch.object(test, 'report_extensively'):
            test.run()
            self.assertFalse(test.report_extensively.called)


class TestSkipping(testtools.TestCase):

    def test_is_skipped(self):

        class WillSkip(tests.SSTBrowserLessTestCase):

            def test_it(self):
                self.skip('test reason')

        test = WillSkip('test_it')
        result = testtools.TestResult()
        test.run(result)
        self.assertIn('test reason', result.skip_reasons)
