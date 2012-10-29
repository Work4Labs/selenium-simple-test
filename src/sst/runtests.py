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
import traceback
from textwrap import dedent

from unittest2 import TestSuite, TextTestRunner, TestCase, SkipTest

from sst import (
    actions,
    config,
    context,
)
from .actions import (
    start, stop, reset_base_url, _set_wait_timeout, take_screenshot,
    get_page_source, EndTest
)
from .context import populate_context


__all__ = ['runtests']


def runtests(test_names, test_dir='.', report_format='console',
             browser_type='Firefox', javascript_disabled=False,
             browsermob_enabled=False, shared_directory=None,
             screenshots_on=False, failfast=False, debug=False,
             webdriver_remote_url=None, browser_version='',
             browser_platform='ANY', session_name=None,
             extended=False):

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
            webdriver_remote_url, screenshots_on, found_tests, failfast, debug,
            extended=extended,
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
        runner = TextTestRunner(verbosity=2, failfast=failfast)
        def run():
            runner.run(alltests)

    if report_format == 'html':
        import HTMLTestRunner
        _make_results_dir()
        fp = file(os.path.join(config.results_directory, 'results.html'), 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp, title='SST Test Report', verbosity=2, failfast=failfast
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
        result.failfast = failfast
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
              webdriver_remote_url, screenshots_on, found, failfast, debug,
              extended=False):
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
                        failfast=failfast, debug=debug, extended=extended
                    )
                )
        else:
            suite.addTest(
                get_case(
                    test_dir, entry, browser_type, browser_version,
                    browser_platform, session_name, javascript_disabled,
                    webdriver_remote_url, screenshots_on,
                    failfast=failfast, debug=debug, extended=extended
                )
            )

    return suite


class SSTTestCase(TestCase):
    """A test case that can use the sst framework."""

    browser_type = 'Firefox'
    browser_version = ''
    browser_platform = 'ANY'
    session_name = None
    javascript_disabled = False
    assume_trusted_cert_issuer = False
    webdriver_remote_url = None

    wait_timeout = 10
    wait_poll = 0.1
    base_url = None

    screenshots_on = False
    debug_post_mortem = False
    extended_report = False

    def setUp(self):
        super(SSTTestCase, self).setUp()
        if self.base_url is not None:
            actions.set_base_url(self.base_url)
        actions._set_wait_timeout(self.wait_timeout, self.wait_poll)
        # Ensures sst.actions will find me
        actions._test = self
        self.start_browser()
        self.addCleanup(self.stop_browser)

    def start_browser(self):
        self.browser, self.browsermob_proxy = start(
            self.browser_type, self.browser_version, self.browser_platform,
            self.session_name, self.javascript_disabled,
            self.assume_trusted_cert_issuer, self.webdriver_remote_url)

    def stop_browser(self):
        stop()

    def take_screenshot(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        tc_name = self.script_name[:-3]
        try:
            filename = 'screenshot-%s-%s.png' % (now, tc_name)
            actions.take_screenshot(filename)
        except Exception:
            # FIXME: Needs to be reported somehow ? -- vila 2012-10-16
            pass
        try:
            # also dump page source
            filename = 'pagesource-%s-%s.html' % (now, tc_name)
            # FIXME: Urgh, config.results_directory is a global set in
            # runtests() -- vila 2012-10-29
            path = os.path.join(config.results_directory, filename)
            with codecs.open(path, 'w', encoding='utf-8') as f:
                f.write(actions.get_page_source())
        except Exception:
            # FIXME: Needs to be reported somehow ? -- vila 2012-10-16
            pass


class SSTScriptTestCase(SSTTestCase):
    """Test case used internally by sst-run and sst-remote."""

    script_dir = '.'
    script_name = None


    def __init__(self, testMethod, context_row=None):
        super(SSTScriptTestCase, self).__init__('runTest')
        self.id = lambda: testMethod
        self.context = context_row

    def __str__(self):
        # Since we use runTest to encapsulate the call to the compiled code, we
        # need to override __str__ to get a proper name reported
        return "%s (%s.%s)" % (self.id(), self.__class__.__module__,
                               self.__class__.__name__)

    def setUp(self):
        self.script_path = os.path.join(self.script_dir, self.script_name)
        sys.path.append(self.script_dir)
        self.addCleanup(sys.path.remove, self.script_dir)
        self._compile_script()
        # The script may override some settings
        if 'JAVASCRIPT_DISABLED' in self.code.co_names:
            # Really ? We don't even check the value ?
            self.javascript_disabled = True
        if 'ASSUME_TRUSTED_CERT_ISSUER' in self.code.co_names:
            # Really ? We don't even check the value ?
            self.assume_trusted_cert_issuer = True
        super(SSTScriptTestCase, self).setUp()
        # Start with default values
        actions.reset_base_url()
        actions._set_wait_timeout(10, 0.1)
        # Possibly inject parametrization from associated .csv file
        context.populate_context(self.context, self.script_path,
                                 self.browser_type, self.javascript_disabled)

    def _compile_script(self):
        with open(self.script_path) as f:
            source = f.read() + '\n'
        self.code = compile(source, self.script_path, 'exec')

    def runTest(self, result=None):
        """Run the test catching exceptions sstnam style."""
        try:
            exec self.code in self.context
        except EndTest:
            pass
        except SkipTest:
            raise
        except:
            exc_class, exc, tb = sys.exc_info()
            self.handle_exception(exc_class, exc, tb)

    def handle_exception(self, exc_class, exc, tb):
        if self.screenshots_on:
            self.take_screenshot()
        if self.debug_post_mortem:
            traceback.print_exception(exc_class, exc, tb)
            pdb.post_mortem()
        if not self.extended_report:
            raise exc_class, exc, tb
        else:
            self.report_extensively(exc_class, exc, tb)

    def report_extensively(self, exc_class, exc, tb):
        original_message = str(exc)
        page_source = 'unavailable'
        current_url = 'unavailable'
        try:
            current_url = actions.get_current_url()
        except Exception:
            pass
        try:
            page_source = actions.get_page_source()
        except Exception:
            pass

        new_message = dedent("""
        Original exception: %s: %s

        Current url: %s

        Page source:

        %s

        """[1:]) % (
               exc.__class__.__name__,
               original_message,
               current_url,
               page_source,
        )
        if isinstance(new_message, unicode):
            new_message = new_message.encode('ascii', 'backslashreplace')
        new_exc = Exception(new_message)
        raise Exception, new_exc, tb


def get_case(test_dir, entry, browser_type, browser_version,
             browser_platform, session_name, javascript_disabled,
             webdriver_remote_url, screenshots_on,
             context=None, failfast=False, debug=False, extended=False):
    context_provided = True
    if context is None:
        context_provided = False
        context = {}

    name = entry[:-3]
    test_name = 'test_%s' % name
    this_test = SSTScriptTestCase(test_name, context)
    this_test.script_dir = test_dir
    this_test.script_name = entry
    this_test.browser_type = browser_type
    this_test.browser_version = browser_version
    this_test.browser_platform = browser_platform
    this_test.webdriver_remote_url = webdriver_remote_url

    this_test.session_name = session_name
    this_test.javascript_disabled = javascript_disabled

    this_test.screenshots_on = screenshots_on
    this_test.debug_post_mortem = debug
    this_test.extended_report = extended

    return this_test


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
