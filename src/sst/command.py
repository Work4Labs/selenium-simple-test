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

import __main__
import logging
import os
import sys
import shutil
import optparse


try:
    import selenium
except ImportError as e:
    print e
    print 'Error: can not import Selenium WebDriver.'
    print 'Selenium 2.x python bindings are required.'
    sys.exit(1)

import sst
from sst import config, actions


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
                            'Ie, etc)'))
    parser.add_option('-j', dest='javascript_disabled',
                      default=False, action='store_true',
                      help='disable javascript in browser')
    parser.add_option('-m', dest='shared_modules',
                      default=None,
                      help='directory for shared modules')
    parser.add_option('-q', dest='quiet', action='store_true',
                      default=False,
                      help='output less debugging info during test run')
    parser.add_option('-V', dest='print_version', action='store_true',
                      default=False,
                      help='print version info and exit')
    parser.add_option('-s', dest='screenshots_on', action='store_true',
                      default=False,
                      help='save screenshots on failures')
    parser.add_option('--failfast',
                      action='store_true', default=False,
                      help='stop test execution after first failure')
    parser.add_option('--debug',
                      action='store_true', default=False,
                      help='drop into debugger on test fail or error')
    parser.add_option('--with-flags', dest='with_flags',
                      help='comma separated list of flags to run '
                      'tests with')
    parser.add_option('--disable-flag-skips', dest='disable_flags',
                      action='store_true', default=False,
                      help='run all tests, disable skipping tests due '
                      'to flags')
    parser.add_option('--extended-tracebacks', dest='extended_tracebacks',
                      action='store_true', default=False,
                      help='Add extra information (page source) to failure '
                      'reports')
    parser.add_option('--collect-only', dest='collect_only',
                      action='store_true', default=False,
                      help='Collect/print cases without running tests')
    parser.add_option('-c', '--custom', action='append', dest='custom',
                      help='Custom parameters')
    parser.add_option('-sl', '--sauce-labs', dest='sauce_labs',
                      action='store_true', default=False,
                      help='Saucelabs username')
    return parser


def get_run_options():
    parser = get_common_options()
    parser.add_option('--browsermob', dest='browsermob',
                      help='enable browsermob proxy (launcher location)')
    parser.add_option('--test',
                      dest='run_tests', action='store_true',
                      default=False,
                      help='run selftests')
    parser.add_option('-x', dest='xserver_headless',
                      default=False, action='store_true',
                      help='run browser in headless xserver')
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


def get_opts_run():
    return get_opts(get_run_options)


def get_opts_remote():
    return get_opts(get_remote_options)


def get_opts(get_options):
    parser = get_options()
    (cmd_opts, args) = parser.parse_args()

    if cmd_opts.print_version:
        print 'SST version: %s' % sst.__version__
        sys.exit()

    # parse custom options
    if cmd_opts.custom:
        custom_opts = {}
        for custom_op in cmd_opts.custom:
            try:
                key, value = custom_op.split('=')
                custom_opts.update({key: value})
            except ValueError:
                print 'Missing "=" in custom option: %s' % custom_op
                sys.exit(1)
        cmd_opts.custom = custom_opts

    run_tests = getattr(cmd_opts, 'run_tests', False)
    if cmd_opts.dir_name == '.' and not args and not run_tests:
        print ('Error: you must supply a test case name or specifiy a '
               'directory.')
        prog = os.path.split(__main__.__file__)[-1]
        print 'run "%s -h" or "%s --help" to see run options.' % (prog, prog)
        sys.exit(1)

    logging.basicConfig(format='    %(levelname)s:%(name)s:%(message)s')
    logger = logging.getLogger('SST')
    if cmd_opts.quiet:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.DEBUG)
    if cmd_opts.disable_flags:
        actions._check_flags = False

    with_flags = cmd_opts.with_flags
    config.flags = [flag.lower() for flag in
                    ([] if not with_flags else with_flags.split(','))]
    return (cmd_opts, args)
