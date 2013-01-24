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


import testtools

from sst import runtests


class TestSSTScriptTestCase(testtools.TestCase):

    def test_id(self):
        """The test id mentions the python class path and the test name."""
        # FIXME: This is a minimal test to cover http://pad.lv/1087606, it
        # would be better to check a results.xml file but we don't have the
        # test infrastructure for that (yet) -- vila 2012-12-07
        test = runtests.SSTScriptTestCase('foo')
        self.assertEqual('sst.runtests.SSTScriptTestCase.foo', test.id())
