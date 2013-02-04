from module import truthiness
from unittest import TestCase

# make sure a regular unittest.TestCase works with runner

class TestUnitTestTestCase(TestCase):
    def test_true(self):
        assert truthiness()
