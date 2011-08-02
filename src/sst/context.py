import os

from sst import actions
from collections import namedtuple

StoredContext = namedtuple(
    'StoredContext',
    'context base_url timeout poll args'
)


def get_sstconfig():
    # a "generated module" which may not be available in sys.modules when this
    # module is imported, so fetch it through a helper function
    import sstconfig
    return sstconfig


def populate_context(
        context, path, browser_type,
        javascript_disabled, arguments=None
    ):
    """Create the execution context for a test"""
    sstconfig = get_sstconfig()

    name = os.path.splitext(
        os.path.split(path)[1]
    )[0]

    context['__file__'] = path
    context['__name__'] = name

    sstconfig._current_context = context
    sstconfig.browser_type = browser_type
    sstconfig.javascript_disabled = javascript_disabled
    sstconfig.__args__ = arguments or {}


def store_context():
    """Store the execution context of test (returned as a namedtuple)
    so that it can be restored later with `restore_context`"""
    sstconfig = get_sstconfig()

    context = sstconfig._current_context
    poll = actions._POLL
    timeout = actions._TIMEOUT
    base_url = actions.BASE_URL
    args = sstconfig.__args__

    return StoredContext(
        context, base_url, timeout, poll,
        args
    )


def restore_context(config):
    """Restore an execution context stored by `store_context`"""
    sstconfig = get_sstconfig()

    sstconfig._current_context = config.context
    actions._POLL = config.poll
    actions._TIMEOUT = config.timeout
    actions.BASE_URL = config.base_url
    sstconfig.__args__ = config.args


def run_test(name, args):
    config = store_context()
    actions.reset_base_url()
    actions.set_wait_timeout(5, 0.1)

    try:
        return _execute_test(name, args)
    finally:
        restore_context(config)


def _execute_test(name, kwargs):
    sstconfig = get_sstconfig()
    current_loc = os.path.dirname(
        sstconfig._current_context['__file__']
    )
    location = os.path.normpath(
        os.path.abspath(
            os.path.join(current_loc, name + '.py')
        )
    )

    context = {}
    populate_context(
        context, location, sstconfig.browser_type,
        sstconfig.javascript_disabled, kwargs
    )

    with open(location) as h:
        exec h.read() in context

    return context.get('RESULT')
