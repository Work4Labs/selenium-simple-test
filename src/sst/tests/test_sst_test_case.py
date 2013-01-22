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

import testtools

from sst import runtests
from sst import config


class FooSSTTestCase(runtests.SSTTestCase):

    def start_browser(self):
        # We do not need to start the browser.
        pass

    def _test_foo(self):
        pass


class TestSSTTestCase(testtools.TestCase):

    def test_results_directory_is_created(self):
        test = FooSSTTestCase('_test_foo')
        test.results_directory = 'foo_test_results'
        test.run()
        self.assertEquals(config.results_directory, 'foo_test_results')
        self.assertTrue(os.path.exists(config.results_directory))
        # Tear down.
        os.removedirs(config.results_directory)
