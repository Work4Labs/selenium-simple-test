Selenium-Simple-Test (SST)
==========================


Requirements:
=============

- Python 2.6 or 2.7

- Selenium WebDriver bindings:
    * $ sudo pip install selenium==2.0.1

- [optional] XML reports requires junitxml:
    * $ sudo pip install junitxml==0.6

- [optional] Running the self-tests requires django 1.1.2:
    * $ sudo pip install django==1.1.2

- [optional] Running headless X-server requires pyvirtualdisplay:
    * $ sudo apt-get install xvfb xserver-xephyr
    * $ sudo pip install pyvirtualdisplay


- You can intall all of these automatically from the requirements.txt file with:
    * $ sudo pip install -r requirements.txt




Running Tests
=============

By default, tests are located in the "/tests" directory under selenium-simple-test.
(you may change this by passing the -d <dir> command-line option)

You can run all tests in this directory by running:

    "./sst-run"

An individual test (file) can be run with just the name of the test.

    "./sst-run mytest"

This runs the test file "tests/mytest.py".




Self-Tests (SST Framework Tests)
================================
SST includes a set of self-tests that include a django project used as the application
under test.  The test django project doesn't have a database, so once you have the
dependencies installed you can execute "./sst-run -d selftests -s" to run the tests.




Experimenting with Selenium and Python
======================================

To experiment with Selenium you can do the following:

    from selenium import webdriver
    b = webdriver.Firefox()
    b.get('http://www.google.com')


