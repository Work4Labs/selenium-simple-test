"""
The `sst.config` module has the following information::

    from sst import config

    # is javascript disabled?
    config.javascript_disabled

    # which browser is being used?
    config.browser_type

    # full path to the shared directory
    config.shared_directory

    # full path to the results directory
    config.results_directory
    
    # is browsermob proxy enabled?
    config.browsermob_enabled

    # flags for the current test run
    config.flags
"""

browser_type = 'Firefox'
_current_context = None
javascript_disabled = False
shared_directory = None
results_directory = None
browsermob_enabled = False
flags = []
__args__ = {}
