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

import ast
import codecs
import datetime
import os
import pdb
import sys

from unittest2 import TestSuite, TextTestRunner, TestCase, SkipTest

from sst import actions, config
from .actions import (
    start, stop, reset_base_url, set_wait_timeout, take_screenshot,
    get_page_source, EndTest
)
from .context import populate_context


__all__ = ['runtests']


def runtests(test_names, test_dir='.', report_format='console',
             browser_type='Firefox', javascript_disabled=False,
             browsermob_enabled=False, shared_directory=None, 
             screenshots_on=False, failfast=False, debug=False,
             webdriver_remote_url=None, browser_version='',
             browser_platform='ANY', session_name=None):

    if test_dir == 'selftests':
        # XXXX horrible hardcoding
        # selftests should be a command instead
        package_dir = os.path.dirname(__file__)
        test_dir = os.path.join(package_dir, 'selftests')

    test_dir = _get_full_path(test_dir)
    if not os.path.isdir(test_dir):
        msg = 'Specified directory %r does not exist' % test_dir
        print msg
        sys.exit(1)

    shared_directory = find_shared_directory(test_dir, shared_directory)
    config.shared_directory = shared_directory
    sys.path.append(shared_directory)

    config.results_directory = _get_full_path('results')
    
    config.browsermob_enabled = browsermob_enabled
    
    found_tests = set()
    test_names = set(test_names)

    suites = (
        get_suite(
            test_names, root, browser_type, browser_version,
            browser_platform, session_name, javascript_disabled,
            webdriver_remote_url, screenshots_on, found_tests, failfast, debug
        )
        for root, _, _ in os.walk(test_dir, followlinks=True)
        if os.path.abspath(root) != shared_directory and
        not os.path.abspath(root).startswith(shared_directory+os.path.sep) and
        not os.path.split(root)[1].startswith('_')
    )

    alltests = TestSuite(suites)

    print ''
    print '  %s test cases loaded\n' % alltests.countTestCases()
    print '----------------------------------------------------------------------'

    if not alltests.countTestCases():
        print 'Error: Did not find any tests'
        sys.exit(1)

    if report_format == 'console':
        runner = TextTestRunner(verbosity=2)
        def run():
            runner.run(alltests)

    if report_format == 'html':
        import HTMLTestRunner
        _make_results_dir()
        fp = file(os.path.join(config.results_directory, 'results.html'), 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp, title='SST Test Report', verbosity=2
        )
        def run():
            runner.run(alltests)

    if report_format == 'xml':
        try:
            import junitxml
        except ImportError:
            print 'Error: Please install junitxml to use XML output'
            sys.exit(1)
        _make_results_dir()
        fp = file(os.path.join(config.results_directory, 'results.xml'), 'wb')
        result = junitxml.JUnitXmlResult(fp)
        result.startTestRun()

        def run():
            try:
                alltests.run(result)
            finally:
                result.stopTestRun()

    try:
        run()
    except KeyboardInterrupt:
        print >> sys.stderr, "Test run interrupted"
    finally:
        missing = test_names - found_tests
        for name in missing:
            msg = 'Warning: test %r not found' % name
            print >> sys.stderr, msg


def _get_full_path(path):
    return os.path.normpath(
        os.path.abspath(
            os.path.join(os.getcwd(), path)
        )
    )


def _make_results_dir():
    try:
        os.makedirs(config.results_directory)
    except OSError:
        pass  # already exists


def find_shared_directory(test_dir, shared_directory):
    """This function is responsible for finding the shared directory.
    It implements the following rule:

    If a shared directory is explicitly specified then that is used.

    The test directory is checked first. If there is a shared directory
    there, then that is used.

    If the current directory is not "above" the test directory then the
    function bails.

    Otherwise it checks every directory from the test directory up to the
    current directory. If it finds one with a "shared" directory then it
    uses that as the shared directory and returns.

    The intention is that if you have 'tests/shared' and 'tests/foo' you
    run `sst-run -d tests/foo` and 'tests/shared' will still be used as
    the shared directory.
    """
    if shared_directory is not None:
        return _get_full_path(shared_directory)

    cwd = os.getcwd()
    default_shared = os.path.join(test_dir, 'shared')
    shared_directory = default_shared
    if not os.path.isdir(default_shared):
        relpath = os.path.relpath(test_dir, cwd)
        if not relpath.startswith('..') and not os.path.isabs(relpath):
            while relpath and relpath != os.curdir:
                this_shared = os.path.join(cwd, relpath, 'shared')
                if os.path.isdir(this_shared):
                    shared_directory = this_shared
                    break
                relpath = os.path.split(relpath)[0]

    return _get_full_path(shared_directory)


def get_suite(test_names, test_dir, browser_type, browser_version,
              browser_platform, session_name, javascript_disabled,
              webdriver_remote_url, screenshots_on, found, failfast, debug):
    suite = TestSuite()
    dir_list = os.listdir(test_dir)

    for entry in dir_list:
        if not entry.endswith('.py'):
            continue
        if test_names and entry[:-3] not in test_names:
            continue
        elif not test_names:
            if entry.startswith('_'):
                # ignore entries starting with underscore unless specified
                continue
        found.add(entry[:-3])

        csv_path = os.path.join(test_dir, entry.replace('.py', '.csv'))
        if os.path.isfile(csv_path):
            # reading the csv file now
            for row in get_data(csv_path):
                # row is a dictionary of variables
                suite.addTest(
                    get_case(
                        test_dir, entry, browser_type, browser_version,
                        browser_platform, session_name, javascript_disabled,
                        webdriver_remote_url, screenshots_on, row,
                        failfast=failfast, debug=debug
                    )
                )
        else:
            suite.addTest(
                get_case(
                    test_dir, entry, browser_type, browser_version,
                    browser_platform, session_name, javascript_disabled,
                    webdriver_remote_url, screenshots_on,
                    failfast=failfast, debug=debug
                )
            )

    return suite


def get_case(test_dir, entry, browser_type, browser_version,
             browser_platform, session_name, javascript_disabled,
             webdriver_remote_url, screenshots_on,
             context=None, failfast=False, debug=False):
    context_provided = context is not None
    context = context or {}
    path = os.path.join(test_dir, entry)

    def setUp(self):
        sys.path.append(test_dir)
        with open(path) as h:
            source = h.read() + '\n'
            self.code = compile(source, path, 'exec')

        js_disabled = javascript_disabled or \
            'JAVASCRIPT_DISABLED' in self.code.co_names
        populate_context(context, path, browser_type, js_disabled)

        original = actions.VERBOSE
        actions.VERBOSE = False
        try:
            reset_base_url()
            set_wait_timeout(10, 0.1)
        finally:
            actions.VERBOSE = original

        assume_trusted_cert_issuer = 'ASSUME_TRUSTED_CERT_ISSUER' in self.code.co_names

        start(browser_type, browser_version, browser_platform,
              session_name, js_disabled, assume_trusted_cert_issuer,
              webdriver_remote_url)

    def tearDown(self):
        sys.path.remove(test_dir)
        stop()

    def test(self):
        if context_provided:
            print 'Loading data row %r' % context['_row_num']
        try:
            exec self.code in context
        except EndTest:
            pass
        except SkipTest:
            raise
        except:
            if screenshots_on:
                now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                tc_name = entry[:-3]
                filename = 'screenshot-%s-%s.png' % (now, tc_name)
                take_screenshot(filename)
                # also dump page source
                filename = 'pagesource-%s-%s.html' % (now, tc_name)
                path = os.path.join(config.results_directory, filename)
                with codecs.open(path, 'w', encoding='utf-8') as f:
                    f.write(get_page_source())
            if debug:
                pdb.post_mortem()
            raise

    def run(self, result=None):
        # moved bits from original implementation of TestCase.run to
        # keep the way it works
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
        TestCase.run(self, result)
        if not result.wasSuccessful() and failfast:
            result.shouldStop = True

    name = entry[:-3]
    test_name = 'test_%s' % name
    FunctionalTest = type(
        'Test%s' % name.title(), (TestCase,),
        {'setUp': setUp, 'tearDown': tearDown,
         test_name: test, 'run': run}
    )
    return FunctionalTest(test_name)


def get_data(csv_path):
    """
    Return a list of data dicts for parameterized testing.

      the first row (headers) match data_map key names
      rows beneath that are filled with data values
    """
    rows = []
    print '  Reading data from %r...' % os.path.split(csv_path)[-1],
    row_num = 0
    with open(csv_path) as f:
        headers = f.readline().rstrip().split('^')
        headers = [header.replace('"', '') for header in headers]
        headers = [header.replace("'", '') for header in headers]
        for line in f:
            row = {}
            row_num += 1
            row['_row_num'] = row_num
            fields = line.rstrip().split('^')
            for header, field in zip(headers, fields):
                try:
                    value = ast.literal_eval(field)
                except ValueError:
                    value = field
                    if value.lower() == 'false':
                        value = False
                    if value.lower() == 'true':
                        value = True
                row[header] = value
            rows.append(row)
    print 'found %s rows' % len(rows)
    return rows
