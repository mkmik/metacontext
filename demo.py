#!/usr/bin/env python
import matchsyntax
matchsyntax.register_match_importer()

import dis
import traceback

import example

try:
    example.test(('test', 1))
except example.TestException:
    e = traceback.format_exc()
    print "GOT TRACEBACK", e
    assert 'File "example.py", line 31, in test' in e
    assert 'raise TestException("let\'s look at the stack trace")' in e

example.other_test(('test', 1))

example.MyActor().run()

print "---------"
dis.dis(example.test)
