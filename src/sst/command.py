#!/usr/bin/env python
#
#   Copyright (c) 2011 Canonical Ltd.
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
import shutil
import optparse


try:
    import selenium
except ImportError as e:
    print e
    print 'Error importing Selenium WebDriver.  Selenium 2.x python bindings are required.'
    sys.exit(1)


usage = """Usage: %prog [testname] [options]

- Calling %prog with testname(s) as arguments will just run
those tests. The testnames should not include '.py' at
the end of the filename.
"""


def clear_old_results():
    try:
        shutil.rmtree('./results/')
    except OSError:
        pass


def get_common_options():
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-d', dest='dir_name',
                      default='.',
                      help='directory of test case files')
    parser.add_option('-r', dest='report_format',
                      default='console',
                      help='results report format (html, xml, console)')
    parser.add_option('-b', dest='browser_type',
                      default='Firefox',
                      help=('select webdriver (Firefox, Chrome, '
                            'InternetExplorer, etc)'))
    parser.add_option('-j', dest='javascript_disabled',
                      default=False, action='store_true',
                      help='disable javascript in browser')
    parser.add_option('-m', dest='shared_modules',
                      default=None,
                      help='directory for shared modules')
    parser.add_option('-q', dest='quiet', action='store_true',
                      default=False,
                      help='output less debugging info during test run')
    parser.add_option('-s', dest='screenshots_on', action='store_true',
                      default=False,
                      help='save screenshots on failures')
    parser.add_option('--failfast',
                      action='store_true', default=False,
                      help="stop test execution after first failure")
    parser.add_option('--debug',
                      action='store_true', default=False,
                      help="drop into debugger on test fail or error")
    return parser


def get_run_options():
    parser = get_common_options()
    parser.add_option('--test',
                      dest='run_tests', action='store_true',
                      default=False,
                      help='run selftests')
    parser.add_option('-x', dest='xserver_headless',
                      default=False, action='store_true',
                      help='run tests in headless xserver')
    return parser
    

def get_remote_options():
    parser = get_common_options()
    parser.add_option('-p', dest='browser_platform',
                      default='ANY',
                      help=('desired platform (XP, VISTA, LINUX, etc), '
                            'when using a remote Selenium RC'))
    parser.add_option('-v', dest='browser_version',
                      default='',
                      help=('desired browser version, when using a '
                            'remote Selenium'))
    parser.add_option('-n', dest='session_name',
                      default=None,
                      help=('identifier for this test run session, '
                            'when using a remote Selenium RC'))
    parser.add_option('-u', dest='webdriver_remote_url',
                      default=None,
                      help=('url to WebDriver endpoint '
                            '(eg: http://host:port/wd/hub), '
                            'when using a remote Selenium RC'))
    return parser
