functest requires the Python selenium package. Running the tests requires
django 1.1.2 installed.


We should be able to get round the invalid ssl certificate problem either by
creating a custom firefox profile and running selenium with that, or by
creating a custom firefox launcher.

http://garbuz.com/2010/07/31/running-selenium-with-custom-firefox-profile/
http://mogotest.com/blog/2010/04/13/how-to-accept-self-signed-ssl-certificates-in-selenium/