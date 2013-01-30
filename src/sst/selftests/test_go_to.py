from sst.actions import *
from sst import runtests


class TestGoto(runtests.SSTTestCase):

    def test_go_to(self):
        go_to('/')
        assert_title('The Page Title')
        assert_url('/')
        go_to('/begin')
        assert_title('The Next Page')
        assert_url('/begin')
