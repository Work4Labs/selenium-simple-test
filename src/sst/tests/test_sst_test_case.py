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

import mock
import testtools

from sst import runtests
from sst import config


class FooSSTTestCase(runtests.SSTTestCase):
    """Test case to use on the tests. All the test methods are private so it's
    not run as part of the unit test suite.

    """

    results_directory = 'foo_test_results'

    # We do not need to start the browser.
    def start_browser(self):
        pass

    def stop_browser(self):
        pass

    def _test_success(self):
        pass

    def _test_failure(self):
        assert False


class TestSSTTestCase(testtools.TestCase):

    def setUp(self):
        super(TestSSTTestCase, self).setUp()
        self.addCleanup(self.remove_results_directory)

    def remove_results_directory(self):
        os.removedirs(config.results_directory)

    def test_results_directory_is_created(self):
        test = FooSSTTestCase('_test_success')
        test.run()
        self.assertEquals(config.results_directory, 'foo_test_results')
        self.assertTrue(os.path.exists(config.results_directory))

    def test_screenshot_and_page_dump_on_failure_enabled(self):
        test = FooSSTTestCase('_test_failure')
        test.screenshots_on = True
        test.take_screenshot_and_page_dump = mock.MagicMock()
        test.run()
        test.take_screenshot_and_page_dump.assert_called_once_with()

    def test_screenshot_and_page_dump_on_failure_disabled(self):
        test = FooSSTTestCase('_test_failure')
        test.screenshots_on = False
        test.take_screenshot_and_page_dump = mock.MagicMock()
        test.run()
        self.assertFalse(test.take_screenshot_and_page_dump.called)
