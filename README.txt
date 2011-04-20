Functional testing with Selenium-Sim-ple-Test (SST)
===================================================

Running the tests requires django 1.1.2 installed:

    * $ sudo pip install django==1.1.2

It also requires selenium 2.0b4 or greater.

    * $ sudo pip install selenium==2.0b4dev

You can do this automatically from the requirements.txt file with:

    * sudo pip install -r requirements.txt


The test django project doesn't have a database so once you have the dependencies
installed you can execute ``./run`` to run the tests.

An individual test (file) can be run with just the name of the test. E.g. to run
just the test for the radio button you do:

  ``./run radio``

This runs the test file ``tests/radio.py``.

Tests are made up of scripts in a 'tests' directory. These scripts are created
by composing actions that drive selenium. You generate the documentation for
the standard actions by running:

  ``python makedocs.py``

This generates the text file "actions.txt".




Experimenting with Selenium and Python
======================================

To experiment with Selenium you can do the following:
    
    from selenium import webdriver
    b = webdriver.Firefox()
    b.get('http://www.google.com')




Handling invalid SSL certificates
=================================

.. note::

  SSO staging now has a valid ssl certificate, so the problem
  described below is no longer blocking us. These notes kept for
  future reference.

We should be able to get round the invalid ssl certificate problem either by
creating a custom firefox profile and running selenium with that, or by
creating a custom firefox launcher.

http://garbuz.com/2010/07/31/running-selenium-with-custom-firefox-profile/
http://mogotest.com/blog/2010/04/13/how-to-accept-self-signed-ssl-certificates-in-selenium/

Official selenium documentation on untrusted SSL certificates:

https://code.google.com/p/selenium/wiki/UntrustedSSLCertificates
