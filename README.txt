Functional testing with functest
================================

functest requires the Python selenium package and the Selenium 2b1 Java server.

Running the tests requires django 1.1.2 installed.

Download the selenium Java package (jar) from:

  http://selenium.googlecode.com/files/selenium-server-standalone-2.0b1.jar

You should place this file in the top level of the project directory (the same
directory as this file).

The easiest way to install the python dependencies is to create a
'virtualenv', which is an isolated python environment that allows you to
install packages without installing them into your system. See
requirements.txt for the packages you will need to install. Once you have
created and activated your virtualenv you install packages with 'pip'. For
example:

* pip install selenium
* pip install django==1.1.2

You can do this automatically from the requirements.txt file with:

* pip install -r requirements.txt

The test django project doesn't have a database so once you have the dependencies
installed you can execute ``./run`` to run the tests.

During test runs selenium output is diverted to a file "selenium.log".


Running tests against pay on staging
====================================

We are using the payments project to drive use cases for ``functest``.

Change directory into ``staging-pay``. The tests require a username (email) and
password to login to SSO. Create a file ``passwords.py`` in the ``staging-pay``
directory, with the following contents::

  username = 'my.username@canonical.com'
  password = 'mypassword'

(``passwords.py`` is ignored by bazaar so you can't accidentally check it
into the repository.)

You can then execute ``./run`` to run the tests against pay.

The tests depend on being able to create new payments with the testconsumer,
which require you to be a member of the ``isd-hackers`` group.


Experimenting with Selenium and Python
======================================

To experiment with Selenium you can do the following:

* Start the selenium server:

  java -jar selenium-server-standalone-2.0b1.jar -trustAllSSLCertificates

* From another terminal window activate the virtualenv (from inside the
  virtualenv directory):

  source bin/activate

* Start the python interactive interpreter:

  python

* Execute the following code:

  from selenium import FIREFOX
  from selenium.remote import connect
  b = connect(FIREFOX)
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
