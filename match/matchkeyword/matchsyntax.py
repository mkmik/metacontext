import ast

from metacontext import Keyword

class NoMatch(Exception):
    """should be in pattern match library"""


class MatchKeyword(Keyword):
    NoMatch = NoMatch

    def __call__(self, pattern):
        return (pattern[0] == 'test', None)

    def translate(self, body, args, var):
        die = ast.Raise(ast.Call(ast.Attribute(ast.Name('match', ast.Load()), 'NoMatch', ast.Load()), [], [], None, None), None, None)

        die.lineno = body[-1].lineno + 1

        body.append(die)
        return ast.While(ast.Name('True', ast.Load()), body, [])


class CaseKeyword(Keyword):
    def translate(self, body, args, var):
        trace = ast.Print(None, [ast.Str("fun trace line: %s" % args.lineno)], True)

        if len(args.args) > 1:
            # implicit tuple
            match_args = [ast.Tuple(args.args, ast.Load())]
        else:
            match_args = args.args

        store = ast.Store()
        mm = ast.Assign([ast.Tuple([ast.Name('__is_match', store),
                                    ast.Name('__x', store)], store)],
                        ast.Call(ast.Name('match', ast.Load()),
                                 match_args, [], None, None))

        brk = ast.copy_location(ast.Break(), body[-1])
        body.append(brk)
        check = ast.If(ast.Name('__is_match', ast.Load()), body, [])

        case_body = [trace, mm, check]

        return case_body


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
