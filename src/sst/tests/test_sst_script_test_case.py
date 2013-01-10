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

import mock
import testtools

from sst import runtests


class TestSSTScriptTestCase(testtools.TestCase):

    script_name = 'test_foo'
    script_code = 'pass'
    test = runtests.SSTScriptTestCase(script_name)

    def setUp(self):
        super(TestSSTScriptTestCase, self).setUp()
        self.test.script_name = self.script_name
        self.test.results_directory = 'tmp/foo_test_results'
        self.test.code = compile(self.script_code+'\n', '<string>', 'exec')
        # We don't need to compile the script because we have already define
        # the code to execute.
        self.test._compile_script = lambda: None
        # We don't need to start the browser.
        self.test.start_browser = lambda: None
        self.test.stop_browser = lambda: None

    @mock.patch.object(runtests.SSTScriptTestCase, 'run_test_script')
    def test_script_is_run(self, mock_run):
        self.test.run()
        mock_run.assert_called_once_with()

class TestSSTScriptTestCaseFailure(TestSSTScriptTestCase):

    script_code = 'assert False'

    @mock.patch.object(runtests.SSTScriptTestCase,
                       'take_screenshot_and_page_dump')
    def test_screenshot_and_page_dump_on_failure_enabled(
            self, mock_screenshot_and_dump):
        self.test.screenshots_on = True
        self.test.run()
        mock_screenshot_and_dump.assert_called_once_with()
