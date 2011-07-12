#!/usr/bin/env python
#
#   Copyright (c) 2011 Canonical Ltd.
#
#   This file is part of: SST (selenium-simple-test)
#   https://launchpad.net/selenium-simple-test
#
#   License: GNU LGPLv3 (http://www.gnu.org/licenses/)
#
#   SST is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Lesser Public License
#   as published by the Free Software Foundation.
#

__all__ = ['runtests']
__version__ = '0.0alpha'

try:
    from .runtests import runtests
except ImportError as e:
    # Selenium not installed
    # this means we can import the __version__
    # for setup.py when we install, without
    # *having* to install selenium first
    def runtests(*args, **kwargs):
        raise e

