import inspect
import sys

# we have to fixup nosetest imports
import metacontext.tests.testcontext
sys.modules['metacontext.tests.testcontext'] = metacontext.tests.testcontext

from metacontext.tests.stest_metacontext import *

for n, f in ((n, f) for n, f in globals().items() if inspect.isfunction(f) and n.startswith('stest_')):
    del globals()[f.func_name]
    f.func_name = f.func_name[1:]
