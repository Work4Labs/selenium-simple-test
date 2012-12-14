#!/bin/bash

# bootstrap and run acceptance selftests with browser.
#
# Invoke script with a browser name as an argument.  
# Available browsers are: Firefox and Chrome (Chromium).
#
# run this script from main directory after getting a branch of SST:
#   $ bzr branch lp:selenium-simple-test
#


if [ "$1" == "Firefox" ]; then
    BROWSER="Firefox"
elif [ "$1" == "Chrome" ]; then 
    BROWSER="Chrome"
elif [ -z "$1" ]; then
    BROWSER="Firefox"
else
    echo "$1 not recognized. (try: $0 Firefox, or:  $0 Chrome)"
    exit
fi

rm -rf ENV results pep8.log pylint.log

virtualenv ENV
source ENV/bin/activate

if [ -d sst-deps ]; then
    cd sst-deps
    bzr pull
    cd ..
else
    bzr branch lp:~ubuntuone-hackers/selenium-simple-test/sst-deps
fi

PATH=sst-deps:$PATH  # so bindings find chromedriver

pip install sst-deps/*.tar.gz

echo "running pep8 checks..."
pep8 --repeat --exclude=.bzr,ENV . > pep8.log
echo "pep8 done."

echo "----------------"
echo "environment info:"
echo "----------------"

python -V
python -c "import django; print 'Django %s' % django.get_version()"
python -c "import selenium; print 'Selenium %s' % selenium.__version__"
./sst-run -V

case "$BROWSER" in
    "Firefox")
        firefox -v
        ./sst-run --test -x -s -r xml -b Firefox
        ;;
    "Chrome")
        ./sst-run --test -x -s -r xml -b Chrome
        ;;
esac

echo "Done."
