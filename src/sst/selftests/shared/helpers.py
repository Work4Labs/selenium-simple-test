import os

from sst.actions import skip


def skip_as_jenkins():
    """Skip test when running as Jenkins user."""
    try:
        user = os.environ['USER']
    except KeyError:
        user = 'notjenkins'
    if user.lower() == 'jenkins':
        skip()
