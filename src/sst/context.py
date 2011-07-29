import os

from sst import actions
from collections import namedtuple

StoredContext = namedtuple(
    'StoredContext',
    'context base_url timeout poll'
)


def get_config():
    # a "generated module" which may not be available in sys.modules when this
    # module is imported, so fetch it through a helper function
    import sstconfig
    return sstconfig


def populate_context(
        context, path, module, browser_type,
        javascript_disabled
    ):
    sstconfig = get_config()

    context['__file__'] = path
    context['__name__'] = os.path.splitext(module)[0]

    sstconfig._current_context = context
    sstconfig.browser_type = browser_type
    sstconfig.javascript_disabled = javascript_disabled


def store_context():
    sstconfig = get_config()

    context = sstconfig._current_context
    poll = actions._POLL
    timeout = actions._TIMEOUT
    base_url = actions.

    return StoredContext(
        context, base_url, timeout, poll
    )


def restore_context(config):
    sstconfig = get_config()

    sstconfig._current_context = config.context
    actions._POLL = config.poll
    actions._TIMEOUT = config.timeout
    actions.BASE_URL = config.base_url


def run_test(name, **kwargs):
    config = store_context()
    actions.reset_base_url()
    actions.set_wait_timeout(5, 0.1)

    try:
        _execute_test(name, **kwargs)
    finally:
        restore_context(config)
