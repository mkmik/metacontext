import ast

from metacontext import MetaContext

class QuoteMetaContext(MetaContext):

    def translate(self, translator, body, args, var):
        ast_sym = translator.gensym()

        MetaContext.templates[ast_sym] = body
        mm = ast.Assign([var], ast.parse('MetaContext.get_template("%s")' % ast_sym, mode='eval').body)

        locals_call = ast.copy_location(ast.Call(ast.Name('locals', ast.Load()), [], [], None, None), body[-1])

        expand = ast.copy_location(ast.Call(ast.Attribute(ast.Name('self', ast.Load()), 'expand', ast.Load()),
                          [ast.Name(var.id, ast.Load()), locals_call], [],  None, None), body[-1])

        ast.fix_missing_locations(expand)
        ast.fix_missing_locations(locals_call)

        expand_expr = ast.copy_location(ast.Expr(expand), body[-1])
        ast.fix_missing_locations(expand_expr)

        return [mm, expand_expr]


class UnquoteBindMetaContext(MetaContext):
    def __init__(self):
        self.bound_vars = {}

    def translate(self, translator, body, args, var):
        if isinstance(var, ast.Tuple):
            for i, v in enumerate(var.elts):
                self.bound_vars[v.id] = args.args[i]
        else:
            self.bound_vars[var.id] = args.args[0]
        return body


def rhs(name):
    return ast.Name(name.id, ast.Load())


def lhs(name):
    return ast.Name(name.id, ast.Store())



quote = QuoteMetaContext()
unquote_bind = UnquoteBindMetaContext()

unquote = object()
unquote_stmts = object()
