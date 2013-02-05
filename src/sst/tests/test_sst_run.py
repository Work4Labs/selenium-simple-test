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
#


import sys
import os
from cStringIO import StringIO

import testtools

from sst import (
    config,
    runtests,
    tests,
)



class SSTBrowserlessTestCase(runtests.SSTScriptTestCase):
    def setUp(self):
        # We don't need to compile the script because we have already defined
        # the code to execute.
        self._compile_script = lambda: None
        self.code = compile(self.script_code + '\n', '<string>', 'exec')
        super(SSTBrowserlessTestCase, self).setUp()
    
    def start_browser(self):
        pass

    def stop_browser(self):
        pass



class TestSSTScriptTestCase(testtools.TestCase):
    
    def setUp(self):
        super(TestSSTScriptTestCase, self).setUp()
        tests.set_cwd_to_tmp(self)
        # capture test output so we don't pollute the test runs
        self.out = StringIO()
        self.patch(sys, 'stdout', self.out)
        self.test = runtests.SSTScriptTestCase('foo')

    def test_attributes(self):
        test = self.test
        
        self.assertEqual(test._testMethodName, 'run_test_script')
        # why is base_url "None" ???
        self.assertIsNone(test.base_url)
        self.assertEqual(test.browser_platform, 'ANY')
        self.assertEqual(test.browser_type, 'Firefox')
        self.assertFalse(test.javascript_disabled)
        self.assertFalse(test.screenshots_on)
        self.assertEqual(test.wait_poll, 0.1)
        self.assertEqual(test.wait_timeout, 10)
        # why is test.shortDescription() "None" ???  --cmg
        #self.assertEqual(test.shortDescription(), 'test_sst_run.SSTStringTestCase.foo')
        self.assertEqual(test.id(), 'sst.runtests.SSTScriptTestCase.foo')


    def test_config(self):
        self.assertIsNone(config._current_context)
        self.assertEqual(config.browser_type, 'Firefox')
        self.assertEqual(config.cache, {})
        self.assertEqual(config.flags, [])
        self.assertFalse(config.javascript_disabled)
        self.assertFalse(config.browsermob_enabled)
        self.assertEqual(os.path.split(config.results_directory)[-1], 'results')
        self.assertEqual(os.path.split(config.shared_directory)[-1], 'shared')


class TestSSTTestCase(testtools.TestCase):
    
    def setUp(self):
        super(TestSSTTestCase, self).setUp()
        
        self.test = SSTBrowserlessTestCase('testing')
        self.test.script_code = 'assert True'
        self.test.results_directory = 'results'
        result = testtools.TestResult()
        self.test.run(result)
        
        tests.set_cwd_to_tmp(self)
        # capture test output so we don't pollute the test runs
        self.out = StringIO()
        self.patch(sys, 'stdout', self.out)


    def test_attributes(self):
        test = self.test
        self.assertEqual(test._testMethodName, 'run_test_script')
        # why is base_url "None" ???  --cmg
        self.assertIsNone(test.base_url)
        self.assertEqual(test.browser_platform, 'ANY')
        self.assertEqual(test.browser_type, 'Firefox')
        self.assertFalse(test.javascript_disabled)
        self.assertFalse(test.screenshots_on)
        self.assertEqual(test.wait_poll, 0.1)
        self.assertEqual(test.wait_timeout, 10)
        # why is test.shortDescription() "None" ???  --cmg
        #self.assertEqual(test.shortDescription(), 'test_sst_run.SSTBrowserlessTestCase.testing')
        self.assertEqual(test.id(), 'test_sst_run.SSTBrowserlessTestCase.testing')


    def test_config(self):
        self.assertIsNone(config._current_context)
        self.assertEqual(config.browser_type, 'Firefox')
        self.assertEqual(config.cache, {})
        self.assertEqual(config.flags, [])
        self.assertFalse(config.javascript_disabled)
        self.assertFalse(config.browsermob_enabled)
        self.assertEqual(os.path.split(config.results_directory)[-1], 'results')
        self.assertEqual(os.path.split(config.shared_directory)[-1], 'shared')
