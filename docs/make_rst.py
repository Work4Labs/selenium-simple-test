#!/usr/bin/env python

# run this script to create an index.rst file for inout to Sphinx.
#
# from the command line run `sphinx-build` against the docs directory:
# $ sphinx-build -b html docs sst_docs


import inspect
import os
import sys
import textwrap

this_dir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(this_dir, '../src'))

from funcrunner import actions


index_text = """

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
* get a copy of the trunk:

    ::

        bzr branch lp:selenium-simple-test

-----------
    License
-----------

SST is Free Open Source Software, licensed under the **GNU LGPLv3**


-------------------------------
    Quickstart on Ubuntu/Debian
-------------------------------

This should be everything you need to get up and running on a fresh install of Ubuntu:

::

    $ sudo apt-get install bzr python-pip
    $ bzr branch lp:selenium-simple-test
    $ cd selenium-simple-test
    $ sudo pip install -r requirements.txt
    $ ./run.py -d examples


--------------------------------------------------
    Quickstart for Selenium2/Webdriver from Python
--------------------------------------------------

SST depends on Selenium (2.x), so first make sure Selenium/Webdriver is working on your system.

 * install selenium package (Python bindings) with pip, easy_install, or however you wish:
 
  * sudo pip install selenium
  * http://pypi.python.org/pypi/selenium

 * make sure it works.
 
  * create a script containing the following webdriver code, and run it:
  
  ::
   
    #!/usr/bin/env python
    from selenium import webdriver
    browser = webdriver.Firefox()
    browser.get('http://www.ubuntu.com/')

 * this should open your Firefox browser and navigate to the Ubuntu homepage.


-----------------------
Example SST test script
-----------------------

a sample test case in SST::

    from funcrunner.actions import *

    goto('http://www.ubuntu.com/')
    title_contains('Ubuntu homepage')
    
    
--------------------------------
Running your first test with SST
--------------------------------

create a .py file in the 'selenium-simple-test/tests' directory, and add your code.

then call your test from the command line, using run.py (located inside your 'selenium-simple-test' direcrory)::

    $./run.py mytest.py
    or
    $ python run.py mytest.py


------------------------
    Running the examples
------------------------

SST ships with a few trivial example scripts.  You can run them like this::

    $./run.py -d examples   


--------------------------
    Running the self-tests
--------------------------

SST ships with a set of self-tests based on a test Django project.

You can run the suite of self tests (and the test django server) like this::

    $./run.py -d selftests -s 


--------------------
Command line options
--------------------

Usage: run.py [testname] 

* Calling run.py without any arguments runs all tests in the local 'test' directory.

* Calling run.py with testname(s) as arguments will just run those tests. The testnames should not include the '.py' at the end of the filename.

* You may optionally create a data file for data-driven testing.  Create a '^' delimited txt data file with the same name as the test, plus the '.csv' extension.  This will run a test using each row in the data file (1st row of data file is variable name mapping)

Options:
  -h, --help        show this help message and exit
  -d DIR_NAME       directory of test case files
  -r REPORT_FORMAT  results report format (html, xml, console)
  -b BROWSER_TYPE   select webdriver (Firefox, Chrome, InternetExplorer, etc)
  -s                launch django server for local SST framework tests
  -x                run tests in headless xserver
  

-------------------------
    Organizing your tests
-------------------------

for logical organization of tests, you can use directories in your filesystem.  SST will recursively walk your directory tree and gather all tests for execution.

for example, a simple test setup might look like::

    /selenium-simple-test
        /mytests
            foo.py
        
and you would call this from the command line::

    $./run.py -d mytests
    

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

    $./run.py -d mytests
    
SST will find all of the tests in subdirectories and execute them.



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
   
"""






with open(os.path.join(this_dir, 'index.rst'), 'w') as h:    
    h.write(index_text)
    


with open(os.path.join(this_dir, 'actions.rst'), 'w') as h:
    def _write(text):
        if text.strip() and text.startswith('\n'):
            text = text[1:]
        text = textwrap.dedent(text or '')
        h.write(text)
        h.write('\n')
    
    foo = """
=====================
    Actions Reference
=====================

"""
    h.write(foo)
    
    
    _write(actions.__doc__)
    _write('\n')
    
    for entry in sorted(actions.__all__):
        member = getattr(actions, entry)
        doc = getattr(member, '__doc__', '')

        if not doc:
            continue

        _write(entry)
        _write('-' * len(entry))
        h.write('\n')

        try:
            spec = inspect.getargspec(member)
        except TypeError:
            pass
        else:
            _write('::')
            spec_text = inspect.formatargspec(*spec)
            h.write('\n   ' + entry + spec_text + '\n\n')

        _write(doc)
        h.write('\n')

        




















