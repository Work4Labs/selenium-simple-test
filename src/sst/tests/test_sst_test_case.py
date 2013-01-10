#!/usr/bin/env python
#
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
import shutil

import mock
import testtools

from sst import runtests, config, tests


class FooSSTTestCase(tests.SSTHeadlessTestCase):
    """Test case to use on the tests. All the test methods are private so it's
    not run as part of the unit test suite.

    """

    results_directory = 'tmp/foo_test_results'

    def _test_success(self):
        pass

    def _test_failure(self):
        assert False

    def _test_skip(self):
        import sst.actions
        sst.actions.skip()


class TestSSTTestCase(testtools.TestCase):

    def setUp(self):
        super(TestSSTTestCase, self).setUp()
        self.addCleanup(self.remove_results_directory)

    def remove_results_directory(self):
        shutil.rmtree(config.results_directory)


class TestResultsDirectory(TestSSTTestCase):

    def test_results_directory_is_created(self):
        test = FooSSTTestCase('_test_success')
        test.run()
        self.assertEquals(config.results_directory, 'tmp/foo_test_results')
        self.assertTrue(os.path.exists(config.results_directory))


class TestScreenshotAndPageDump(TestSSTTestCase):
        
    @mock.patch.object(runtests.SSTTestCase, 'take_screenshot_and_page_dump')
    def test_screenshot_and_page_dump_on_failure_enabled(
            self, mock_screenshot_and_dump):
        test = FooSSTTestCase('_test_failure')
        test.screenshots_on = True
        test.run()
        mock_screenshot_and_dump.assert_called_once_with()

    @mock.patch.object(runtests.SSTTestCase, 'take_screenshot_and_page_dump')
    def test_screenshot_and_page_dump_on_failure_disabled(
            self, mock_screenshot_and_dump):
        test = FooSSTTestCase('_test_failure')
        test.screenshots_on = False
        test.run()
        self.assertFalse(mock_screenshot_and_dump.called)


class TestResults(TestSSTTestCase):
        
    def test_is_skipped(self):
        test = FooSSTTestCase('_test_skip')
        result = testtools.TestResult()
        test.run(result)
        self.assertEqual([], result.errors)
        self.assertEqual([], result.failures)
        self.assertFalse(tests.wasSuccessful)
        self.assertEqual({}, result.skip_reasons)
