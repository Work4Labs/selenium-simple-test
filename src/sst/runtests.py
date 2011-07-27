#!/usr/bin/env python
#
#   Copyright (c) 2011 Canonical Ltd.
#
#   This file is part of: SST (selenium-simple-test)
#   https://launchpad.net/selenium-simple-test
#
#   License: GNU LGPLv3 (http://www.gnu.org/licenses/)
#
#   SST is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Lesser Public License
#   as published by the Free Software Foundation.
#

import ast
import os
import sys

from unittest import TestSuite, TextTestRunner, TestCase

from .actions import start, stop, reset_base_url


__unittest = True

__all__ = ['runtests']


def runtests(test_names, test_dir='tests', report_format='console',
             browser_type='Firefox', javascript_disabled=False,
             ):

    if test_dir == 'selftests':
        # XXXX horrible hardcoding
        # selftests should be a command instead
        package_dir = os.path.dirname(__file__)
        test_dir = os.path.join(package_dir, 'selftests')

    if not os.path.isdir(test_dir):
        msg = 'Specified directory %r does not exist' % (test_dir,)
        raise IOError(msg)

    found_tests = set()
    test_names = set(test_names)

    suites = (
        get_suite(
            test_names, root, browser_type, javascript_disabled,
            found_tests
        )
        for root, _, _ in os.walk(test_dir)
    )

    alltests = TestSuite(suites)

    if not alltests.countTestCases():
            print "Error: Didn't find any tests"
            sys.exit(1)

    if report_format == 'console':
        runner = TextTestRunner(verbosity=2)
        runner.run(alltests)

    if report_format == 'html':
        import HTMLTestRunner
        fp = file('results.html', 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp, title='SST Test Report', verbosity=2
        )
        runner.run(alltests)

    if report_format == 'xml':
        try:
            import junitxml
        except ImportError:
            print 'Please install junitxml to use XML output'
            sys.exit(1)
        fp = file('results.xml', 'wb')
        result = junitxml.JUnitXmlResult(fp)
        result.startTestRun()
        alltests.run(result)
        result.stopTestRun()

    missing = test_names - found_tests
    for name in missing:
        msg = "Warning: test %r not found" % name
        print >> sys.stderr, msg


def get_suite(test_names, test_dir, browser_type, javascript_disabled, found):
    test_path = os.path.abspath(os.path.join(os.curdir, test_dir))

    suite = TestSuite()
    dir_list = os.listdir(test_path)

    for entry in dir_list:
        if not entry.endswith('.py'):
            continue
        if test_names and entry[:-3] not in test_names:
            continue
        elif not test_names:
            if entry.startswith('_'):
                # ignore entries that start with an underscore unless explcitly specified
                continue
        found.add(entry[:-3])

        csv_path = os.path.join(test_path, entry.replace('.py', '.csv'))
        if os.path.isfile(csv_path):
            # reading the csv file now
            for row in get_data(csv_path):
                # row is a dictionary of variables
                suite.addTest(
                    get_case(test_path, entry, browser_type, javascript_disabled, row)
                )
        else:
            suite.addTest(
                get_case(test_path, entry, browser_type, javascript_disabled)
            )

    return suite


def get_case(test_dir, entry, browser_type, javascript_disabled, context=None):
    context = context or {}
    path = os.path.join(test_dir, entry)
    def setUp(self):
        sys.path.append(test_dir)
        reset_base_url()
        start(browser_type, javascript_disabled)
    def tearDown(self):
        sys.path.remove(test_dir)
        stop()
    def test(self):
        if context:
            print 'Loading data row %s' % context['_row_num']
        with open(path) as h:
            source = h.read() + '\n'
            code = compile(source, path, 'exec')
            exec code in context

    name = entry[:-3]
    test_name = 'test_%s' % name
    FunctionalTest = type(
        'Test%s' % name.title(), (TestCase,),
        {'setUp': setUp, 'tearDown': tearDown,
         test_name: test}
    )
    return FunctionalTest(test_name)



def get_data(csv_path):
    """
    Return a list of data dicts for parameterized testing.

      the first row (headers) match data_map key names
      rows beneath that are filled with data values
    """
    rows = []
    print 'Reading data from %s...' % csv_path,
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

