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
    assert 'File "example.py", line 22, in test' in e
    assert 'raise TestException("let\'s look at the stack trace")' in e

print "---------"
dis.dis(example.test)
