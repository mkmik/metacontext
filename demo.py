#!/usr/bin/env python
import matchsyntax
matchsyntax.register_match_importer()

import dis

import example

example.test(('test', 1))

print "---------"
dis.dis(example.test)
