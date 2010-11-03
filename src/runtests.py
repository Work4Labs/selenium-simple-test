#! /usr/bin/env python
import os
import sys

this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(this_dir)

from funcrunner import runtests

runtests()
