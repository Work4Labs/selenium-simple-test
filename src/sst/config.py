"""
The `sst.config` module has the following information::

    from sst import config

    # is javascript disabled?
    config.javascript_disabled

    # which browser is being used?
    config.browser_type

    # full path to the shared directory
    config.shared_directory

"""

browser_type = None
_current_context = None
javascript_disabled = False
shared_directory = None
__args__ = {}
