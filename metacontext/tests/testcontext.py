#- LANGUAGE compile-time-context-manager -#

from metacontext import Keyword
from metacontext.template import quote, unquote, unquote_stmts, unquote_bind


class timeit(Keyword):
    """Example metacontext manager built only for tests.
    The same functionality could be provided with a normal context manager.

    """

    def template(self, translator, body, args, var):
        with quote() as q:
            print "TIMING"
            unquote_stmts(body)
        return q
