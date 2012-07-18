import ast

from metacontext import Keyword

class NoMatch(Exception):
    """should be in pattern match library"""


class MatchKeyword(Keyword):
    NoMatch = NoMatch

    def __call__(self, msg, pattern):
        if msg[0] == pattern[0]:
            return (True, msg)
        else:
            return (False, None)

    def translate(self, translator, body, args, var):
        translator.stack[-1]['match_msg_Name'] = args.args[0]

        die = ast.Raise(ast.Call(ast.Attribute(ast.Name('match', ast.Load()), 'NoMatch', ast.Load()), [], [], None, None), None, None)

        die.lineno = body[-1].lineno + 1

        body.append(die)
        return ast.While(ast.Name('True', ast.Load()), body, [])


class CaseKeyword(Keyword):
    def translate(self, translator, body, args, var):
        trace = ast.Print(None, [ast.Str("fun trace line: %s" % args.lineno)], True)

        try:
            match_msg_node = translator.stack[-2]['match_msg_Name']
        except (IndexError, KeyError):
            raise SyntaxError("with case() should be nested in a with match() construct")

        store = ast.Store()
        mm = ast.Assign([ast.Tuple([ast.Name('__is_match', store),
                                    ast.Name('__x', store)], store)],
                        ast.Call(ast.Name('match', ast.Load()),
                                 [match_msg_node] + args.args, [], None, None))

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
