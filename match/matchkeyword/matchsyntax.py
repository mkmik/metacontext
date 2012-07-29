#- LANGUAGE compile-time-context-manager -#

import ast

from metacontext import MetaContext
from metacontext.template import quote, unquote, unquote_stmts, unquote_bind
import patternmatching

class NoMatch(Exception):
    """should be in pattern match library"""

class MatchMetaContext(MetaContext):
    NoMatch = NoMatch

    def __call__(self, msg, pattern):
        res = patternmatching.match(pattern, msg)
        return (res[0], res[1:])

    def template(self, translator, body, args, var):
        translator.stack[-1]['match_msg_Name'] = args.args[0]
        translator.stack[-1]['case_is_match_sym'] = translator.gensym()
        translator.stack[-1]['case_x_sym'] = translator.gensym()

        with quote() as q:
            while True:
                unquote_stmts(body)
                raise match.NoMatch()

        return q

class CaseMetaContext(MetaContext):
    def template(self, translator, body, args, var):
        try:
            match_msg_node = translator.stack[-2]['match_msg_Name']
        except (IndexError, KeyError):
            raise SyntaxError("with case() should be nested in a with match() construct")

        if var:
            if isinstance(var, ast.Tuple):
                bound_vars = var
            else:
                bound_vars = ast.Tuple([var], ast.Store())
        else:
            bound_vars = ast.Name('__x__', ast.Store())

        with quote() as q:
            with unquote_bind(bound_vars) as __x:
                __is_match, __x = match(unquote([match_msg_node] + args.args))
                if __is_match:
                    unquote_stmts(body)
                    break

        return q

match = MatchMetaContext()
case = CaseMetaContext()
