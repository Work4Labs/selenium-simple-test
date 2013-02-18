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

from sst import runtests


class TestFindCases(testtools.TestCase):

    def setUp(self):
        super(TestFindCases, self).setUp()
        self.test_dir = '/tmp/cases/'
        self.addCleanup(shutil.rmtree, self.test_dir)
        os.mkdir(self.test_dir)
        file_names = set((
            'test_a_real_test.py',
            'test_a_real_test2.py',
            'script.py',
            'not_a_test',
            'test_not_a_test.p',
            '_hidden.py',
        ))
        for fn in file_names:
            with open(os.path.join(self.test_dir, fn), 'w'):
                pass


    def test_find_cases_single_name(self):
        find_files = (
            'test_a_real_test.py',
        )
        found = runtests.find_cases(find_files, self.test_dir)
        self.assertSetEqual(set(find_files), found)


    def test_find_cases_multi_name(self):
        find_files = (
            'test_a_real_test.py',
            'script.py',
        )
        found = runtests.find_cases(find_files, self.test_dir)
        self.assertSetEqual(set(find_files), found)


    def test_find_cases_glob(self):
        find_files = (
            'test_a_real_test.py',
            'test_a_real_test2.py',
        )
        found = runtests.find_cases(('test_a_real_test*', ), self.test_dir)
        self.assertSetEqual(set(find_files), found)
        found = runtests.find_cases(('test_a_real_test*.py', ), self.test_dir)
        self.assertSetEqual(set(find_files), found)
        found = runtests.find_cases(('*_a_real_test*', ), self.test_dir)
        self.assertSetEqual(set(find_files), found)

