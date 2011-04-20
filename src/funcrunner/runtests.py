import os
import sys
import time

from unittest import TestSuite, TextTestRunner, TestCase

from .actions import start, stop, reset_base_url, waitfor


__unittest = True

__all__ = ['runtests']

USAGE = """runtests [testname]

- Calling runtests without any arguments runs all tests.

- Calling runtests with testname(s) will just run those
tests. The testnames should not include the '.py' at
the end of the filename.

- You may optionally create a data file for data-driven 
testing.  Create a '^' delimited txt data file with the same 
name as the test, plus the '.csv' extension.  This will 
run a test using each row in the data file (1st row of data
file is variable name mappings)
"""



def runtests():
    args = sys.argv[1:]
    if '-h' in args or '--help' in args:
        print USAGE
        sys.exit(0)

    suite = get_suite(args)
   
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)


def get_suite(argv):
    args = set(argv)
    argv = set(argv)

    test_directory = os.path.abspath(os.path.join(os.curdir, 'tests'))
    if not test_directory in sys.path:
        sys.path.append(test_directory)

    suite = TestSuite()
    for entry in os.listdir('tests'):
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
        path = os.path.join('tests', entry.replace('.py', '.csv'))
        if os.path.isfile(path):
            for row in get_data(path):  # reading the csv file now
                suite.addTest(get_case(entry, row))  # row is a dictionary of variables
        else:
            suite.addTest(get_case(entry))
    if argv:
        print 'The following tests were not found: %s' % (
            ' '.join(argv)
        )
        sys.exit(1)
    return suite
    
    

def get_case(entry, context=None):
    context = context or {}
    path = os.path.join('tests', entry)
    def setUp(self):
        reset_base_url()
        start()
    def tearDown(self):
        stop()
    def test(self):
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



def get_data(path):
    """
    Return a list of data dicts for parameterized testing.
    
      the first row (headers) match data_map key names
      rows beneath that are filled with data values
    """
    rows = []
    print 'Reading data from %s...' % path,
    with open(path) as f:
        headers = f.readline().rstrip().split('^')
        for line in f:
            if not line.startswith('#'):
                fields = line.rstrip().split('^')
                row = {}
                for header, field in zip(headers, fields):
                    if field == 'false':
                        field = False
                    if field == 'true':
                        field = True
                    row[header] = field
                rows.append(row)
    print ' found %s rows' % len(rows)
    return rows

