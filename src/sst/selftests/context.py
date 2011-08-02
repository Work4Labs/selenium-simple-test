import os
import sstconfig

assert locals() == sstconfig._current_context
assert sstconfig.browser_type
assert sstconfig.__args__ == {}
assert not sstconfig.javascript_disabled
assert __name__ == 'context'
assert __file__.endswith('context.py')

thisdir = os.path.dirname(__file__)
assert sstconfig.shared_directory == os.path.join(thisdir, 'shared')
