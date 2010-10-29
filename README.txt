functest requires the Python selenium package and the selenium 2a7 Java server.

Running the tests requires django 1.1.2 installed.

Download the selenium Java package (jar) from:

  http://selenium.googlecode.com/files/selenium-server-standalone-2.0a7.jar

The easiest way to install the python dependencies is to create a
'virtualenv', which is an isolated python environment that allows you to
install packages without installing them into your system. See
requirements.txt for the packages you will need to install. Once you have
created and activated your virtualenv you install packages with 'pip'. For
example:

* pip install selenium
* pip install django==1.1.2

To experiment you can do the following:

* Start the selenium server:

  java -jar selenium-server-standalone-2.0a4.jar -trustAllSSLCertificates

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


We should be able to get round the invalid ssl certificate problem either by
creating a custom firefox profile and running selenium with that, or by
creating a custom firefox launcher.

http://garbuz.com/2010/07/31/running-selenium-with-custom-firefox-profile/
http://mogotest.com/blog/2010/04/13/how-to-accept-self-signed-ssl-certificates-in-selenium/

Official selenium documentation on untrusted SSL certificates:

https://code.google.com/p/selenium/wiki/UntrustedSSLCertificates