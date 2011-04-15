#!/usr/bin/env python

import inspect
import os
import sys
import textwrap

this_dir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(this_dir, 'src'))

from funcrunner import actions
   

header = """\
<html>
<head>
    <title>Selenium Simple Test (SST)</title>
    <style type="text/css">
        body {
            background-color: #FFFFFF;
            color: #000000;
            font-family: Verdana, Helvetica, Arial, sans-serif;
            font-size: 12px;
            padding: 10px;
            margin: 20px;
        }
        pre {
            font-family: "Courier New", Courier, monospace;
            font-size: 13px;
            margin: 20px;
        }
        p {
            font-family: "Courier New", Courier, monospace;
            font-size: 13px;
            padding-left: 8px;
        }
        h1 {
            font-size: 20px;
            background: #FF9966;
            padding-left: 8px;
        }
        h2 {
            font-size: 16px;
            background: #CCCCCC;
            padding-left: 8px;
            margin-top: 40px;
        }
        h3 {
            font-size: 14px;
            padding-left: 8px;
        }
    </style>
</head>
<body>
"""


footer = """\
</body>
</html>
"""


about_text = """

<p>
Selenium Simple Test (SST) is a web test framework that uses a simple 
Python DSL to generate functional GUI tests.
</p>

<p>
Tests are made up of scripts, created by composing actions that drive a browser
via selenium.  You have the flexibilty of the full Python language, along with
a convenient set of functions of simplify web testing.
</p>

<p>
At runtime, scripts are converted to a standard Python unittest suite and executed.
</p>

<h2>Functional testing with SST</h2>

<h3>Example test script</h3>

<pre>
    from funcrunner.actions import *


    set_base_url('http://www.google.com/')
    goto('/finance')

    url_is('/finance')
    fails(url_is, '/foo')

    title_is('Google Finance: Stock market quotes, news, currency conversions & more')

    textfield_write(get_element(name='q'), 'IBM')
    button_click(get_element(tag='input', value='Get quotes'))

    url_contains('IBM')
    
    
</pre>    

<h1>Actions</h1>
"""



with open(os.path.join(this_dir, 'selenium-simple-test.html'), 'w') as h:
    def _write(text):
        h.write(text)
        h.write('\n')

    _write(header)
    
    _write('<h1>Selenium Simple Test (SST)</h1>') 
    
    _write('<img src="http://code.google.com/p/selenium/logo?cct=1301309575"></img>')
    
    _write('<h3>DSL for functional web tests</h3>')
    
    _write('<hr />')
    
    _write(about_text)
    
    _write('<pre>{0}</pre>'.format(actions.__doc__))
    
    for entry in actions.__all__:
        member = getattr(actions, entry)
        doc = getattr(member, '__doc__', '')

        if not doc:
            continue
        
        _write('<h2>{0}</h2>'.format(entry))

        try:
            spec = inspect.getargspec(member)
        except TypeError:
            pass
        else:
            spec_text = inspect.formatargspec(*spec)
            _write('<pre><strong>{0}{1}</strong></pre>'.format(entry, spec_text))
            
        _write('<p>{0}</p>'.format(doc))
        
    _write(footer)
    
    