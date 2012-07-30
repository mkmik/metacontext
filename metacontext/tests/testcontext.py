#- LANGUAGE compile-time-context-manager -#

import ast

from metacontext import MetaContext
from metacontext.template import quote, unquote_stmts, unquote_bind, rhs


class timeit(MetaContext):
    """Example metacontext manager built only for tests.
    The same functionality could be provided with a normal context manager.

    """

    def template(self, translator, body, args, var):
        logging = [k.value for k in args.keywords if k.arg == 'log']
        if logging:
            logging = logging[0]
            with quote() as log:
                with unquote_bind(logging, rhs(var)) as (_logging, res):
                    if _logging:
                        print "Took", res
        else:
            log = []

        time_module = ast.Name(translator.gensym(), ast.Load())

        with quote() as q:
            with unquote_bind(var, time_module) as (res, _time):
                import time as _time
                _start = _time.time()
                unquote_stmts(body)
                res = _time.time() - _start
                unquote_stmts(log)
        return q
