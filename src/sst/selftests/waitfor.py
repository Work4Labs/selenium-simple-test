from sst.actions import *
from time import time

def get_condition(result=True, wait=0, raises=False):
    initial = time()
    def condition():
        if time() > initial + wait:
            return result
        if raises:
            raise AssertionError('not yet')
        return False
    return condition

goto('/')

waitfor(get_condition(True))
fails(waitfor, get_condition(False))

waitfor(get_condition(raises=True))
fails(waitfor, get_condition(False, raises=True))

