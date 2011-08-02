import os

from sst import actions, config
from collections import namedtuple

StoredContext = namedtuple(
    'StoredContext',
    'context base_url timeout poll args'
)



def populate_context(
        context, path, browser_type,
        javascript_disabled, arguments=None
    ):
    """Create the execution context for a test"""

    name = os.path.splitext(
        os.path.split(path)[1]
    )[0]

    context['__file__'] = path
    context['__name__'] = name

    config._current_context = context
    config.browser_type = browser_type
    config.javascript_disabled = javascript_disabled
    config.__args__ = arguments or {}


def store_context():
    """Store the execution context of test (returned as a namedtuple)
    so that it can be restored later with `restore_context`"""
    context = config._current_context
    poll = actions._POLL
    timeout = actions._TIMEOUT
    base_url = actions.BASE_URL
    args = config.__args__

    return StoredContext(
        context, base_url, timeout, poll,
        args
    )


def restore_context(context_config):
    """Restore an execution context stored by `store_context`"""
    config._current_context = context_config.context
    actions._POLL = context_config.poll
    actions._TIMEOUT = context_config.timeout
    actions.BASE_URL = context_config.base_url
    config.__args__ = context_config.args


def run_test(name, args):
    context_config = store_context()
    actions.reset_base_url()
    actions.set_wait_timeout(5, 0.1)

    try:
        return _execute_test(name, args)
    finally:
        restore_context(context_config)


def _execute_test(name, kwargs):
    current_loc = os.path.dirname(
        config._current_context['__file__']
    )
    location = os.path.normpath(
        os.path.abspath(
            os.path.join(current_loc, name + '.py')
        )
    )

    context = {}
    populate_context(
        context, location, config.browser_type,
        config.javascript_disabled, kwargs
    )

    with open(location) as h:
        exec h.read() in context

    return context.get('RESULT')
