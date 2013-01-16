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

import os

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
        # is modified as a side-effect, this is violates isolation
        # -- vila 2013-01-15
        from sst import config
        self.assertTrue(os.path.exists(config.results_directory))
        self.assertTrue(os.path.exists('results'))


class TestScreenshotAndPageDump(testtools.TestCase):

    def setUp(self):
        super(TestScreenshotAndPageDump, self).setUp()
        tests.set_cwd_to_tmp(self)

    def get_screenshot_test(self, with_screenshots):
        class ForScreenshotTests(tests.SSTBrowserLessTestCase):

            nb_calls = 0
            screenshots_on = with_screenshots

            def take_screenshot_and_page_dump(self):
                """Counts the calls.

                We don't have a browser so won't be able to do a real
                screenshot anyway.
                """
                self.nb_calls += 1

            def test_it(self):
                """An always failing test."""
                self.assertTrue(False)

        return ForScreenshotTests('test_it')

    def test_screenshot_and_page_dump_on_failure_enabled(self):
        test = self.get_screenshot_test(True)
        result = testtools.TestResult()
        test.run(result)
        self.assertEquals(1, test.nb_calls)

    def test_screenshot_and_page_dump_on_failure_disabled(self):
        test = self.get_screenshot_test(False)
        result = testtools.TestResult()
        test.run(result)
        self.assertEquals(0, test.nb_calls)


class TestSkipping(testtools.TestCase):

    def test_is_skipped(self):

        class WillSkip(tests.SSTBrowserLessTestCase):

            def test_it(self):
                self.skip('test reason')

        test = WillSkip('test_it')
        result = testtools.TestResult()
        test.run(result)
        self.assertIn('test reason', result.skip_reasons)
