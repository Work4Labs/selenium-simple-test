import os
import sys

this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(this_dir, 'src'))

from sst import __version__

import os



NAME = 'sst'
PACKAGES = ['sst', 'sst.selftests']
SCRIPTS = ['sst-run']
DESCRIPTION = 'Selenium Simple Test Framework'
URL = 'https://launchpad.net/selenium-simple-test'

readme = os.path.join(this_dir, 'README.txt')
LONG_DESCRIPTION = open(readme).read()

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Testing',
    'Topic :: Internet :: WWW/HTTP :: Browsers',
]

AUTHOR = 'Canonical ISD Team'
AUTHOR_EMAIL = 'test@example.com'
KEYWORDS = ("selenium test testing").split(' ')

params = dict(
    name=NAME,
    version=__version__,
    packages=PACKAGES,
    scripts=SCRIPTS,
    package_dir={'': 'src'},
    package_data={'sst.selftests': ['*.csv', '_package/*', 'shared/*',
                                    'subdirectory/*']},

    # metadata for upload to PyPI
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords=KEYWORDS,
    url=URL,
    classifiers=CLASSIFIERS,
)

from distutils.core import setup
setup(**params)
