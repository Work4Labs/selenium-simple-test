#!/bin/bash

# bootstrap and run acceptance selftests with firefox.
#
# run this from main directory after getting a branch of SST:
#   $ bzr branch lp:selenium-simple-test

rm -rf results ENV

virtualenv ENV
source ENV/bin/activate

if [ -d sst-deps ]; then
  cd sst-deps
  bzr pull
  cd ..
else
  bzr branch lp:~ubuntuone-hackers/selenium-simple-test/sst-deps
fi

pip install sst-deps/*.tar.gz

echo "----------------"
echo "environment info:"
echo "----------------"
python -V
python -c "import django; print 'Django %s' % django.get_version()"
python -c "import selenium; print 'Selenium %s' % selenium.__version__"
./sst-run -V
firefox -v

./sst-run --test -x -s -r xml

echo "Done."
