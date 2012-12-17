#!/bin/bash

# bootstrap and run acceptance selftests with browser.
#
# Invoke script with a browser name as an argument.
# Available browsers are: Firefox and Chrome (Chromium).
#
# run this script from main directory after getting a branch of SST:
#   $ bzr branch lp:selenium-simple-test
#


while [ $# -gt 0 ]; do  # until you run out of parameters
    case "$1" in
        --bootstrap)
            BOOTSTRAP=1
            ;;
        --flake8)
            FLAKE8=1
            ;;
        -u|--unit)
            UNIT=1
            ;;
        -a|--acceptance)
            BROWSER="$2"
            shift
            if [[ "$BROWSER" == "Firefox" || "$BROWSER" == "firefox" ]]; then
                BROWSER="Firefox"
            elif [[ "$BROWSER" == "Chrome" || "$BROWSER" == "chrome" ]]; then
                BROWSER="Chrome"
            else
                echo "browser format $1 not recognized."
                echo "(try: -a Firefox, or: $0 -a Chrome)"
                exit
            fi
            ;;
    esac
    shift  # check next set of parameters
done

if [ -n "$BOOTSTRAP" ]; then
    echo "cleaning up..."
    rm -rf ENV results *.log *.xml
    echo "getting dependencies..."
    if [ -d sst-deps ]; then
        cd sst-deps
        bzr pull
        cd ..
    else
        bzr branch lp:~ubuntuone-hackers/selenium-simple-test/sst-deps
    fi
    echo "creating virtualenv..."
    virtualenv ENV
    source ENV/bin/activate
    echo "installing modules from depenencies branch..."
    pip install sst-deps/*.tar.gz
else
    source ENV/bin/activate
fi

echo "setting path..."
PATH=sst-deps:$PATH  # so bindings find chromedriver

if [ -n "$FLAKE8" ]; then
    echo "running flake8 (pyflakes/pep8) checks..."
    flake8 src/ docs/ sst-* *.py  > flake8.log
fi

echo "-----------------"
echo "environment info:"
echo "-----------------"

python -V
python -c "import django; print 'Django %s' % django.get_version()"
python -c "import selenium; print 'Selenium %s' % selenium.__version__"
./sst-run -V

if [ -n "$UNIT" ]; then
     nosetests --with-xunit -e ENV -e testproject
fi

if [ -n "$BROWSER" ]; then
    if [ "$BROWSER" == "Firefox" ]; then
        firefox -v
    fi
    ./sst-run --test -x -s -r xml -b $BROWSER --extended-tracebacks
fi

echo "Done."
