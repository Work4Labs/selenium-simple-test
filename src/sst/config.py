#
#   Copyright (c) 2011-2013 Canonical Ltd.
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


"""
The `sst.config` module has the following information::

    from sst import config

    # is javascript disabled?
    config.javascript_disabled

    # which browser is being used?
    config.browser_type

    # full path to the shared directory
    config.shared_directory

    # full path to the results directory
    config.results_directory

    # is browsermob proxy enabled?
    config.browsermob_enabled

    # is the test running on SauceLabs?
    config.saucelabs_enabled

    # flags for the current test run
    config.flags

    # A per test cache. A dictionary that is cleared at the start of each test.
    config.cache
"""

browser_type = 'Firefox'
_current_context = None
javascript_disabled = False
shared_directory = None
results_directory = None
browsermob_enabled = False
saucelabs_enabled = False
flags = []
__args__ = {}
cache = {}
