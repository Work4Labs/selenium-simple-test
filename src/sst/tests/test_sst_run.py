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
import shutil

import testtools

from sst import (
    config,
    runtests,
    tests,
)



class TestSSTTestCase(testtools.TestCase):
    
    def setUp(self):
        super(TestSSTTestCase, self).setUp()       
        self.test = tests.SSTBrowserLessTestCase('run')
        self.addCleanup(shutil.rmtree, config.results_directory)
        self.result = testtools.TestResult()
        self.test.run(self.result)

    
    def test_results(self):
        test = self.test
        result = self.result
        self.assertEqual(result.testsRun, 1)
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
        self.assertEqual(result.skipped, [])


    def test_attributes(self):
        test = self.test
        self.assertEqual(test._testMethodName, 'run')
        # why is base_url "None" ???  --cmg
        self.assertIsNone(test.base_url)
        self.assertEqual(test.browser_platform, 'ANY')
        self.assertEqual(test.browser_type, 'Firefox')
        self.assertFalse(test.javascript_disabled)
        self.assertFalse(test.screenshots_on)
        self.assertEqual(test.wait_poll, 0.1)
        self.assertEqual(test.wait_timeout, 10)
        self.assertEqual(test.shortDescription(), 'sst.tests.SSTBrowserLessTestCase.run')
        self.assertEqual(test.id(), 'sst.tests.SSTBrowserLessTestCase.run')


    def test_config(self):
        self.assertIsNone(config._current_context)
        self.assertEqual(config.browser_type, 'Firefox')
        self.assertEqual(config.cache, {})
        self.assertEqual(config.flags, [])
        self.assertFalse(config.javascript_disabled)
        self.assertFalse(config.browsermob_enabled)
        self.assertEqual(os.path.split(config.results_directory)[-1], 'results')

