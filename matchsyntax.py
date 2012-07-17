import ast

from syntaxtranslator import Keyword


class match(Keyword):
    def translate(self, body, args, var):
        return ast.If(ast.Name('True', ast.Load()), body, [])


class case(Keyword):
    def translate(self, body, args, var):
        trace = ast.Print(None, [ast.Str("fun trace line: %s" % args.lineno)], True)
        body.insert(0, trace)

        return ast.If(ast.Name('True', ast.Load()), body, [])

