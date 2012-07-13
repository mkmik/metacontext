#!/usr/bin/env python
import matchsyntax
matchsyntax.register_match_importer()

import example

example.test(('test', 1))
