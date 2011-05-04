Functional testing with Selenium-Simple-Test (SST)
===================================================


Requirements:
=============

- Python 2.6+

- SST requires selenium 2.0b4dev or newer:

    * $ sudo pip install selenium==2.0b4dev
    
    
- Running the self-tests requires django 1.1.2:

    * $ sudo pip install django==1.1.2


- You can intall these automatically from the requirements.txt file with:

    * sudo pip install -r requirements.txt



Running Tests
=============

By default, tests are located in the "/tests" directory under selenium-simple-test.
(you may change this by passing the -d <dir> command-line option)

You can run all tests in this directory by running:

    "./run.py"
    or
    "python run.py"

An individual test (file) can be run with just the name of the test. 

    "./run.py googlefinance"

This runs the test file "tests/googlefinance.py".



Command Line Options (for run.py)
=================================

Options:
  -h, --help   show this help message and exit
  -d DIR_NAME  directory of test case files
  -r           generate html report instead of console output
  -s           launch django server for local SST framework tests
  
  

Self-Tests (SST Framework Tests)
================================
SST includes a set of self-tests that include a django project used as the application 
under test.  The test django project doesn't have a database, so once you have the 
dependencies installed you can execute "./run -d selftests -s" to run the tests.



Experimenting with Selenium and Python
======================================

To experiment with Selenium you can do the following:
    
    from selenium import webdriver
    b = webdriver.Firefox()
    b.get('http://www.google.com')


