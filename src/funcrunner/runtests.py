import os
import sys
import time

from selenium import FIREFOX
from selenium.remote import connect

from unittest import TestSuite, TextTestRunner, TestCase

from .actions import start, stop, reset_base_url, waitfor


__unittest = True

__all__ = ['runtests']

USAGE = """runtests [testname]

Calling runtests without any arguments runs all tests.
Calling runtests with testname(s) will just run those
tests. The testnames should not include the '.py' at
the end of the filename.
"""


def selenium_is_up():
    try:
        b = connect(FIREFOX)
    except:
        return False
    b.close()
    return True


def runtests():
    args = sys.argv[1:]
    if '-h' in args or '--help' in args:
        print USAGE
        sys.exit(0)

    # find tests before waiting for selenium
    # as finding tests can fail
    suite = get_suite(args)

    waitfor(selenium_is_up, timeout=25, poll=1.5,
            msg='selenium to start')

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)


def get_suite(argv):
    args = set(argv)

    suite = TestSuite()
    for entry in os.listdir('tests'):
        if not entry.endswith('.py'):
            continue
        if args and entry[:-3] not in args:
            continue
        if args:
            argv.remove(entry[:-3])
        suite.addTest(get_case(entry))
    if argv:
        print 'The following tests were not found: %s' % (
            ' '.join(argv)
        )
        sys.exit(1)
    return suite


def get_case(entry):
    path = os.path.join('tests', entry)
    def setUp(self):
        reset_base_url()
        start()
    def tearDown(self):
        stop()
    def test(self):
        context = {}
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
