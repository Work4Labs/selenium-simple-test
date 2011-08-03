
==============================
    SST - selenium-simple-test
==============================


--------------------------------------------
    Automated Web Test Framework with Python
--------------------------------------------

selenium-simple-test (SST) is a web test framework that uses a simple
Python DSL to generate functional GUI tests.

Tests are made up of scripts, created by composing actions that drive a browser
via selenium/webdriver.  You have the flexibilty of the full Python language,
along with a convenient set of functions to simplify web testing.

SST consists of:

 * convenient actions (functions) in Python
 * test case loader (converts to xUnit style cases)
 * test runner (unittest)
 * data parameterization/injection
 * XML/HTML/Console report output

At runtime, scripts are converted to a standard Python unittest suite and executed.


------------
    Download
------------

Coming soon!


--------
    Code
--------

* `Launchpad Project <https://launchpad.net/selenium-simple-test>`_
* `Browse the Source (Trunk) <http://bazaar.launchpad.net/~canonical-isd-qa/selenium-simple-test/trunk/files>`_
* get a copy of the trunk::

      bzr branch lp:selenium-simple-test


-----------
    License
-----------

SST is Free Open Source Software, **Apache2** Licensed.


-------------------------------
    Quickstart on Ubuntu/Debian
-------------------------------

This should be everything you need to get up and running on a fresh install of Ubuntu::

    $ sudo apt-get install bzr python-pip
    $ bzr branch lp:selenium-simple-test
    $ cd selenium-simple-test
    $ sudo pip install -r requirements.txt
    $ ./sst-run -d examples


--------------------------------------------------
    Quickstart for Selenium2/Webdriver from Python
--------------------------------------------------

SST depends on Selenium (2.x), so first make sure Selenium/Webdriver is working on your system.

 * install selenium package (Python bindings) with pip, easy_install, or however you wish:

  * sudo pip install selenium
  * http://pypi.python.org/pypi/selenium

 * make sure it works.

  * create a script containing the following webdriver code, and run it::

    #!/usr/bin/env python
    from selenium import webdriver
    browser = webdriver.Firefox()
    browser.get('http://www.ubuntu.com/')

 * this should open your Firefox browser and navigate to the Ubuntu homepage.


-----------------------
Example SST test script
-----------------------

a sample test case in SST::

    from sst.actions import *

    goto('http://www.ubuntu.com/')
    title_contains('Ubuntu homepage')


--------------------------------
Running your first test with SST
--------------------------------

Create a .py file in the 'selenium-simple-test/tests' directory, and add your code.

Then call your test from the command line, using sst-run (located inside your
'selenium-simple-test' directory)::

    $./sst-run mytest.py
    or
    $ python sst-run mytest.py


------------------------
    Running the examples
------------------------

SST ships with a few trivial example scripts.  You can run them like this::

    $./sst-run -d examples


--------------------------
    Running the self-tests
--------------------------

SST ships with a set of self-tests based on a test Django project.

You can run the suite of self tests (and the test django server) like this::

    $./sst-run --test


--------------------
Command line options
--------------------

Usage: sst-run [testname]

* Calling sst-run without any arguments runs all tests in the local 'tests' directory.

* Calling sst-run with testname(s) as arguments will just run those tests. The
  testnames should not include the '.py' at the end of the filename.

* You may optionally create a data file for data-driven testing. Create a '^'
  delimited txt data file with the same name as the test, plus the '.csv'
  extension. This will run a test using each row in the data file (1st row of
  data file is variable name mapping)

Options:
  -h, --help         show this help message and exit
  -d DIR_NAME        directory of test case files
  -r REPORT_FORMAT   results report format (html, xml, console)
  -b BROWSER_TYPE    select webdriver (Firefox, Chrome, InternetExplorer, etc)
  -j                 disable javascript in browser
  -s                 launch django server for local SST framework tests
  -x                 run tests in headless xserver
  -m SHARED_MODULES  directory for shared modules
  -q                 output less debugging info during test run
  --test             run selftests
  --failfast         stop test execution after first failure


-------------------------
    Organizing your tests
-------------------------

For logical organization of tests, you can use directories in your filesystem.
SST will recursively walk your directory tree and gather all tests for
execution.

For example, a simple test setup might look like::

    /selenium-simple-test
        /mytests
            foo.py

and you would call this from the command line::

    $./sst-run -d mytests


a more complex setup might look like::

    /selenium-simple-test
        /mytests
            /project_foo
                /feature_foo
                    foo.py
            /project_bar
                feature_bar.py
                feature_baz.py

and you would still call this from the command like::

    $./sst-run -d mytests

SST will find all of the tests in subdirectories and execute them. SST won't look
in directories starting with an underscore. This allows you to put Python packages
directly in your test directories if you want. A better option is to use the
shared directory.


-----------------
 Shared directory
-----------------

XXXX

----------------------
 The sst.config module
----------------------

XXXX


-----------------
    Related links
-----------------

* `Python Unittest <http://docs.python.org/library/unittest.html>`_
* `Selenium Project Home <http://selenium.googlecode.com>`_
* `Selenium WebDriver (from 'Architecture of Open Source Applications') <http://www.aosabook.org/en/selenium.html>`_

----

---------------------
    Actions reference
---------------------

.. toctree::
   :maxdepth: 1

   actions

