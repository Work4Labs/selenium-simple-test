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


import os
import sys
import time

from unittest import TestSuite, TextTestRunner, TestCase

from .actions import start, stop, reset_base_url, waitfor


__unittest = True

__all__ = ['runtests']




def runtests(test_names, test_dir='tests', report_format='console'):
    suite = get_suite(test_names, test_dir)
    
    if report_format == 'console':
        runner = TextTestRunner(verbosity=2)
        runner.run(suite)
        
    if report_format == 'html':
        import HTMLTestRunner
        fp = file('results.html', 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='SST Test Report', verbosity=2)
        runner.run(suite)
        
    if report_format == 'xml':
        try:
            import junitxml
        except ImportError:
            print 'Please install junitxml to use XML output'
            sys.exit(1)
        fp = file('results.xml', 'wb')
        result = junitxml.JUnitXmlResult(fp)
        result.startTestRun()
        suite.run(result)
        result.stopTestRun()

    


def get_suite(test_names, test_dir):
    args = set(test_names)
    argv = set(test_names)

    test_path = os.path.abspath(os.path.join(os.curdir, test_dir))
    if not test_path in sys.path:
        sys.path.append(test_path)

    suite = TestSuite()
    
    try:
        listdir = os.listdir(test_dir)
    except OSError:
        print 'The test directory was not found'
        sys.exit(1)
    
    for entry in listdir:
        if not entry.endswith('.py'):
            continue
        if args and entry[:-3] not in args:
            continue
        elif not args:
            if entry.startswith('_'):
                # ignore entries that start with an underscore unless
                # they are explcitly specified
                continue
        if args:
            argv.remove(entry[:-3])
        csv_path = os.path.join(test_dir, entry.replace('.py', '.csv'))
        if os.path.isfile(csv_path):
            for row in get_data(csv_path):  # reading the csv file now
                suite.addTest(get_case(test_dir, entry, row))  # row is a dictionary of variables
        else:
            suite.addTest(get_case(test_dir, entry))
    if argv:
        print 'The following tests were not found: %s' % (
            ' '.join(argv)
        )
        sys.exit(1)
    return suite
    
    

def get_case(test_dir, entry, context=None):
    context = context or {}
    path = os.path.join(test_dir, entry)
    def setUp(self):
        reset_base_url()
        start()
    def tearDown(self):
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
    FunctionalTest = type('Test%s' % name.title(), (TestCase,),
                          {'setUp': setUp, 'tearDown': tearDown,
                           test_name: test})
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
                    value = eval(field)
                except NameError:
                    value = field
                    if value.lower() == 'false':
                        value = False
                    if value.lower() == 'true':
                        value = True
                row[header] = value
            rows.append(row)
    print 'found %s rows' % len(rows)
    return rows

