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

from sst import runtests


class SSTHeadlessTestCase(runtests.SSTTestCase):
    """A specialized test class for tests around xvfb."""

    # We don't use a browser here so disable its use to speed the tests
    # (i.e. the browser won't be started)
    def start_browser(self):
        pass

    def stop_browser(self):
        pass
