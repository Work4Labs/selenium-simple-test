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

from sst import tests
from sst import runtests


def _make_empty_files(dir):
    file_names = (
        'test_a_real_test.py',
        'test_a_real_test2.py',
        'script.py',
        'not_a_test',
        'test_not_a_test.p',
        '_hidden.py',
    )
    os.mkdir(dir)
    for fn in file_names:
        with open(os.path.join(dir, fn), 'w'):
            pass


class TestFindCases(testtools.TestCase):

    def setUp(self):
        super(TestFindCases, self).setUp()
        tests.set_cwd_to_tmp(self)
        self.cases_dir = os.path.join(self.test_base_dir, 'cases')

    def test_runtests_find_cases_multi_name(self):
        _make_empty_files(self.cases_dir)
        find_files = (
            'test_a_real_test.py',
            'script.py',
        )
        found = runtests.find_cases(find_files, self.cases_dir)
        self.assertSetEqual(set(find_files), found)

    def test_runtests_find_cases_single_name(self):
        _make_empty_files(self.cases_dir)
        find_files = (
            'test_a_real_test.py',
        )
        found = runtests.find_cases(find_files, self.cases_dir)
        self.assertSetEqual(set(find_files), found)

    def test_runtests_find_cases_glob(self):
        _make_empty_files(self.cases_dir)
        find_files = (
            'test_a_real_test.py',
            'test_a_real_test2.py',
        )
        found = runtests.find_cases(('test_a_real_test*', ), self.cases_dir)
        self.assertSetEqual(set(find_files), found)
        found = runtests.find_cases(('test_a_real_test*.py', ), self.cases_dir)
        self.assertSetEqual(set(find_files), found)
        found = runtests.find_cases(('*_a_real_test*', ), self.cases_dir)
        self.assertSetEqual(set(find_files), found)

    def test_runtests_find_cases_glob_and_name(self):
        _make_empty_files(self.cases_dir)
        find_files = (
            'test_a_real_test.py',
            'test_a_real_test2.py',
            'script.py',
        )
        found = runtests.find_cases(('test_*', 'script.py'), self.cases_dir)
        self.assertSetEqual(set(find_files), found)

    def test_runtests_find_cases_none_found(self):
        _make_empty_files(self.cases_dir)
        find_files = []
        found = runtests.find_cases(('xNOMATCHx', ), self.cases_dir)
        self.assertSetEqual(set(find_files), found)
        self.assertEqual(len(found), 0)
