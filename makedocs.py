#!/usr/bin/env python
import os
import sys

this_dir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(this_dir, 'src'))

from funcrunner import actions

with open(os.path.join(this_dir, 'actions.txt'), 'w') as h:
    h.write(actions.__doc__ or '')
    h.write('\n\n')

    for entry in actions.__all__:
        doc = getattr(getattr(actions, entry), '__doc__', '')
        if not doc:
            continue
        h.write(entry)
        h.write('\n')
        h.write('=' * len(entry))
        h.write('\n\n')
        h.write(doc)
        h.write('\n\n')
