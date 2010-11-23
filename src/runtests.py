#! /usr/bin/env python
import os
import sys

this_dir = os.path.abspath(os.path.dirname(__file__))
current_dir = os.path.abspath(os.getcwd())
sys.path.append(this_dir)
sys.path.append(current_dir)

from funcrunner import runtests

runtests()
