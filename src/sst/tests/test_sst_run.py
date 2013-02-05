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

import os

import testtools

from sst import runtests
from sst import config



class TestSSTScriptTestCase(testtools.TestCase):

    def test_attributes(self):
        test = runtests.SSTScriptTestCase('foo')
        self.assertEqual(test._testMethodName, 'run_test_script')
        # why is base_url "None" ???
        #self.assertIsNone(test.base_url)
        self.assertEqual(test.browser_platform, 'ANY')
        self.assertEqual(test.browser_type, 'Firefox')
        self.assertFalse(test.javascript_disabled)
        self.assertFalse(test.screenshots_on)
        self.assertEqual(test.wait_poll, 0.1)
        self.assertEqual(test.wait_timeout, 10)
        # why is test.shortDescription() "None" ???
        #self.assertEqual(test.shortDescription(), 'sst.runtests.SSTTestCase.foo')
        self.assertEqual('sst.runtests.SSTScriptTestCase.foo', test.id())
    
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

    def test_attributes(self):
        test = runtests.SSTTestCase('run')
        self.assertEqual(test._testMethodName, 'run')
        # why is base_url "None" ???
        #self.assertIsNone(test.base_url)
        self.assertEqual(test.browser_platform, 'ANY')
        self.assertEqual(test.browser_type, 'Firefox')
        self.assertFalse(test.javascript_disabled)
        self.assertFalse(test.screenshots_on)
        self.assertEqual(test.wait_poll, 0.1)
        self.assertEqual(test.wait_timeout, 10)
        self.assertEqual(test.shortDescription(), 'sst.runtests.SSTTestCase.run')
        self.assertEqual('sst.runtests.SSTTestCase.run', test.id())
        
    def test_config(self):
        self.assertIsNone(config._current_context)
        self.assertEqual(config.browser_type, 'Firefox')
        self.assertEqual(config.cache, {})
        self.assertEqual(config.flags, [])
        self.assertFalse(config.javascript_disabled)
        self.assertFalse(config.browsermob_enabled)
        self.assertEqual(os.path.split(config.results_directory)[-1], 'results')
        self.assertEqual(os.path.split(config.shared_directory)[-1], 'shared')

