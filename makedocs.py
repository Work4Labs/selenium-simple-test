#!/usr/bin/env python
import inspect
import os
import sys
import textwrap

this_dir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(this_dir, 'src'))

from funcrunner import actions

with open(os.path.join(this_dir, 'actions.txt'), 'w') as h:
    def _write(entry):
        entry = textwrap.dedent(entry or '')
        h.write(entry)
        h.write('\n')

    _write(actions.__doc__)

    for entry in actions.__all__:
        member = getattr(actions, entry)
        doc = getattr(member, '__doc__', '')
        if not doc:
            continue
        _write(entry)
        _write('-' * len(entry))
        h.write('\n')

        try:
            spec = inspect.getargspec(member)
        except TypeError:
            pass
        else:
            _write('::')
            spec_text = inspect.formatargspec(*spec)
            h.write('    ' + entry + spec_text + '\n\n')
        _write(doc)
        _write('\n')
