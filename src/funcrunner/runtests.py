import os

from unittest import TestSuite, TextTestRunner, TestCase

from .actions import start, stop, reset_base_url


__unittest = True

__all__ = ['runtests']


def runtests():
    runner = TextTestRunner(verbosity=2)
    suite = get_suite()
    runner.run(suite)


def get_suite():
    suite = TestSuite()
    for entry in os.listdir('tests'):
        if not entry.endswith('.py'):
            continue
        suite.addTest(get_case(entry))
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
