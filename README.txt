Selenium-Simple-Test (SST)
==========================

:Home: https://launchpad.net/selenium-simple-test
:Author: Copyright (c) 2011 Canonical Ltd.
:License: Apache License, Version 2.0


Automated Web Test Framework with Python
========================================

selenium-simple-test (SST) is a web test framework that uses a simple
Python DSL to generate functional GUI tests.

Tests are made up of scripts, created by composing actions that drive a browser
via selenium/webdriver.  You have the flexibilty of the full Python language,
along with a convenient set of functions to simplify web testing.

SST consists of:

 * convenient actions (functions) in Python
 * test case loader (converts to xUnit style cases)
 * test runner (unittest2)
 * data parameterization/injection
 * XML/HTML/Console report output

At runtime, scripts are converted to a standard Python unittest suite and executed.


Install
=======

SST can be pip installed!

    pip install -U sst

Or you can download the current release from the `pypi page
<http://pypi.python.org/pypi/sst>`_.

The current development version can be found at:

* `Launchpad Project <https://launchpad.net/selenium-simple-test>`_
* `Browse the Source (Trunk)
  <http://bazaar.launchpad.net/~canonical-isd-qa/selenium-simple-test/trunk/files>`_
* get a copy of the trunk::

      bzr branch lp:selenium-simple-test


Requirements:
=============

- Python 2.6 or 2.7

- Selenium WebDriver bindings:
    * $ sudo pip install selenium

- unittest2 test framework
    * $ sudo apt-get install python-unittest2

  Not all distributions package unittest2. You
  may need to do:
    * $ sudo pip install unittest2

- [optional] XML reports requires junitxml:
    * $ sudo pip install junitxml==0.6

- [optional] Running the self-tests requires django 1.1.2:
    * $ sudo pip install django==1.1.2

- [optional] Running headless X-server requires pyvirtualdisplay:
    * $ sudo apt-get install xvfb xserver-xephyr
    * $ sudo pip install pyvirtualdisplay

- You can intall all of these automatically from the requirements.txt file with:
    * $ sudo pip install -r requirements.txt

SST is primarily being developed on Linux, specifically Ubuntu. It should work
fine on other platforms but any issues (or even better - patches) should be
reported on the launchpad project.
