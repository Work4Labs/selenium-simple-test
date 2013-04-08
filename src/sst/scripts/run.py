#!/usr/bin/env python
#
#   Copyright (c) 2011-2012 Canonical Ltd.
#
#   This file is part of: SST (selenium-simple-test)
#   https://launchpad.net/selenium-simple-test
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#


import datetime
import os
import socket
import subprocess
import sys
import time
import traceback
import urllib

import sst
from sst import runtests
from sst.command import get_opts_run, clear_old_results


def main():
    cmd_opts, args = get_opts_run()

    print '--------------------------------------------------------------'
    print 'starting SST...'

    cleanups = []

    if cmd_opts.browsermob and cmd_opts.run_tests:
        print 'Warning: can not record local traffic from django testproject'

    if cmd_opts.browsermob:
        browsermob_process = run_browsermob_server(cmd_opts.browsermob)

        def browsermob_cleanup():
            browsermob_process.kill()
            browsermob_process.wait()

        cleanups.append(('\nkilling browsermob proxy...', browsermob_cleanup))

    if cmd_opts.run_tests:
        cmd_opts.dir_name = 'selftests'
        run_django()
        cleanups.append(('\nkilling django...', kill_django))

    if cmd_opts.xserver_headless:
        from sst.xvfbdisplay import Xvfb
        print '\nstarting virtual display...'
        display = Xvfb(width=1024, height=768)
        display.start()
        cleanups.append(('\nstopping virtual display...', display.stop))

    if not cmd_opts.quiet:
        print ''
        print '  date time: %s' \
            % datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print '  test directory: %r' % cmd_opts.dir_name
        print '  report format: %r' % cmd_opts.report_format
        print '  browser type: %r' % cmd_opts.browser_type
        print '  javascript disabled: %r' % cmd_opts.javascript_disabled
        print '  browswermob proxy launcher: %r' % cmd_opts.browsermob
        print '  shared directory: %r' % cmd_opts.shared_modules
        print '  screenshots on error: %r' % cmd_opts.screenshots_on
        print '  failfast: %r' % cmd_opts.failfast
        print '  debug: %r' % cmd_opts.debug
        print '  headless xserver: %r' % cmd_opts.xserver_headless
        print '  custom options: %r' % cmd_opts.custom
        print ''

    try:
        clear_old_results()
        runtests.runtests(
            args,
            test_dir=cmd_opts.dir_name,
            collect_only=cmd_opts.collect_only,
            report_format=cmd_opts.report_format,
            browser_type=cmd_opts.browser_type,
            javascript_disabled=cmd_opts.javascript_disabled,
            browsermob_enabled=bool(cmd_opts.browsermob),
            shared_directory=cmd_opts.shared_modules,
            screenshots_on=cmd_opts.screenshots_on,
            failfast=cmd_opts.failfast,
            debug=cmd_opts.debug,
            extended=cmd_opts.extended_tracebacks,
            custom_options=cmd_opts.custom
        )
    finally:

        print '--------------------------------------------------------------'
        for desc, cmd in cleanups:
            # Run cleanups, displaying but not propagating exceptions
            try:
                print desc
                cmd()
            except Exception:
                print traceback.format_exc()


def run_django():
    """Start django server for running local self-tests."""
    manage_file = './src/testproject/manage.py'
    url = 'http://localhost:8000/'

    if not os.path.isfile(manage_file):
        print 'Error: can not find the django testproject.'
        print '%r does not exist' % manage_file
        print 'you must run self-tests from the dev branch or package source.'
        sys.exit(1)
    try:
        import django
    except ImportError:
        print 'Error: can not find django module.'
        print 'you must have django installed to run the test project.'
        sys.exit(1)
    subprocess.Popen([manage_file, 'runserver'],
                     stderr=open(os.devnull, 'w'),
                     stdout=open(os.devnull, 'w')
                     )
    print '--------------------------------------------------------------'
    print 'waiting for django to come up...'
    attempts = 30
    for count in xrange(attempts):
        try:
            resp = urllib.urlopen(url)
            if resp.code == 200:
                break
        except IOError:
            time.sleep(0.2)
            if count >= attempts - 1:  # timeout
                print 'Error: can not get response from %r' % url
                raise
    print 'django found. continuing...'


def kill_django():
    try:
        urllib.urlopen('http://localhost:8000/kill_django')
    except IOError:
        pass


def run_browsermob_server(path_to_bmob_server):
    try:
        process = subprocess.Popen([path_to_bmob_server, ],
                                   stderr=open(os.devnull, 'w'),
                                   stdout=open(os.devnull, 'w')
                                   )
    except Exception as e:
        print 'Error: proxy not started'
        print e
        sys.exit(1)
    print '--------------------------------------------------------------'
    print 'waiting for browsermob proxy to come up...'
    attempts = 30
    for count in xrange(attempts):
        try:
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_.settimeout(1)
            socket_.connect(('localhost', 8080))
            socket_.close()
            break
        except socket.error:
            time.sleep(0.2)
            if count >= attempts - 1:  # timeout
                print 'Error: browsermob proxy not started'
                sys.exit(1)
    print 'browsermob proxy found. continuing...'
    return process


if __name__ == '__main__':
    main()
