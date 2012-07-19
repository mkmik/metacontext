#- LANGUAGE compile-time-context-manager -#

import ast

from metacontext import Keyword
from metacontext.template import quote, unquote, unquote_stmts
import patternmatching

class NoMatch(Exception):
    """should be in pattern match library"""

class MatchKeyword(Keyword):
    NoMatch = NoMatch

    def __call__(self, msg, pattern):
        res = patternmatching.match(pattern, msg)
        return (res[0], res[1:])

    def translate(self, translator, body, args, var):
        translator.stack[-1]['match_msg_Name'] = args.args[0]
        translator.stack[-1]['case_is_match_sym'] = translator.gensym()
        translator.stack[-1]['case_x_sym'] = translator.gensym()

        die = ast.Raise(ast.Call(ast.Attribute(ast.Name('match', ast.Load()), 'NoMatch', ast.Load()), [], [], None, None), None, None)

        # This kind of hacks are unfortunately necessary
        # because otherwise the line number table will contain negative deltas which are
        # encoded as unsigned bytes in co_lntab and will cause to skip forward the
        # line numbering by ~200 lines
        # TODO: create a generic line fixup routine which works better than ast.fix_missing_locations
        die.lineno = body[-1].lineno + 1

        body.append(die)
        return ast.While(ast.Name('True', ast.Load()), body, [])


class CaseKeyword(Keyword):
    def xxxtranslate(self, translator, body, args, var):
        try:
            match_msg_node = translator.stack[-2]['match_msg_Name']
        except (IndexError, KeyError):
            raise SyntaxError("with case() should be nested in a with match() construct")

        is_match_sym = translator.stack[-2]['case_is_match_sym']
        x_sym = translator.stack[-2]['case_x_sym']

        store = ast.Store()

        if var:
            if isinstance(var, ast.Tuple):
                bound_vars = var
            else:
                bound_vars = ast.Tuple([var], store)
        else:
            bound_vars = ast.Name(x_sym, store)

        mm = ast.Assign([ast.Tuple([ast.Name(is_match_sym, store),
                                    bound_vars], store)],
                        ast.Call(ast.Name('match', ast.Load()),
                                 [match_msg_node] + args.args, [], None, None))

        brk = ast.copy_location(ast.Break(), body[-1])
        body.append(brk)
        check = ast.If(ast.Name(is_match_sym, ast.Load()), body, [])

        case_body = [mm, check]

        return case_body


    def template(self, translator, body, args, var):
        try:
            match_msg_node = translator.stack[-2]['match_msg_Name']
        except (IndexError, KeyError):
            raise SyntaxError("with case() should be nested in a with match() construct")

        with quote() as q:
            __is_match, __x = match(unquote([match_msg_node] + args.args))
            if __is_match:
                unquote_stmts(body)
                break

        return q

match = MatchKeyword()
case = CaseKeyword()


# while True:
#     is_match, x = match(('some', ANY, 'pattern'))
#     if is_match:
#         <case-body>
#         break

#     is_match, a, b = match(('other', ANY, ANY'))
#     if is_match:
#         <case-body>
#         break

#     raise NoMatch()  # or smth
