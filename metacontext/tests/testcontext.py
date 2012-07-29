#- LANGUAGE compile-time-context-manager -#

import ast

from metacontext import Keyword
from metacontext.template import quote, unquote_stmts, unquote_bind


class timeit(Keyword):
    """Example metacontext manager built only for tests.
    The same functionality could be provided with a normal context manager.

    """

    def template(self, translator, body, args, var):
        var_rhs = ast.Name(var.id, ast.Load())
        with quote() as log:
            with unquote_bind(var_rhs) as res:
                print "Took", res

        if not any(self.evaluate(k.value) for k in args.keywords if k.arg == 'log'):
            log = []

        with quote() as q:
            with unquote_bind(var) as res:
                import time as _time
                _start = _time.time()
                unquote_stmts(body)
                res = _time.time() - _start
                unquote_stmts(log)
        return q
