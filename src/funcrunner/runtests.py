
import os
import sys
import time

from unittest import TestSuite, TextTestRunner, TestCase

from .actions import start, stop, reset_base_url, waitfor


__unittest = True

__all__ = ['runtests']




def runtests(test_names, test_dir='tests', run_report=False):
    suite = get_suite(test_names, test_dir)
    if run_report:
        import HTMLTestRunner
        fp = file('results.html', 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='SST Test Report', verbosity=2)
    else:
        runner = TextTestRunner(verbosity=2)
    runner.run(suite)
    


def get_suite(test_names, test_dir):
    args = set(test_names)
    argv = set(test_names)

    test_path = os.path.abspath(os.path.join(os.curdir, test_dir))
    if not test_path in sys.path:
        sys.path.append(test_path)

    suite = TestSuite()
    
    for entry in os.listdir(test_dir):
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

