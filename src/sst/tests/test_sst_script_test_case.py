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

    def test_script_is_run(self):
        test = runtests.SSTScriptTestCase('test_foo')
        test.run_test_script = mock.MagicMock()
        test.run()
        test.run_test_script.assert_called_once_with()

    def test_screenshot_and_page_dump_on_failure_enabled(self):
        test = runtests.SSTScriptTestCase('test_foo')
        test.screenshots_on = True
        test.code = 'assert False'
        # We don't need to compile the script because we have already define
        # the code to execute.
        test._compile_script = lambda: None
        test.take_screenshot_and_page_dump = mock.MagicMock()
        test.run()
        test.take_screenshot_and_page_dump.assert_called_once_with()
