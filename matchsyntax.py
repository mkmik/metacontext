import ast
import sys

from syntaxtranslator import Translator, TranslatorImportHook


class MatchStatementTranslator(Translator):
    def translate(self, tree):
        return MatchTransformer().visit(tree)


class MatchTransformer(ast.NodeTransformer):
    def if_template(self):
        return ast.parse("if True: pass").body[0]

    def visit_With(self, node):
        node = self.generic_visit(node)

        if node.context_expr.func.id == 'match':
            res = ast.copy_location(self.if_template(), node)
            res.body = [self.visit(i) for i in node.body]
            return res
        elif node.context_expr.func.id == 'case':
            res = ast.copy_location(self.if_template(), node)

            trace = ast.copy_location(ast.Print(None, [ast.Str("fun trace line: %s" % node.lineno)], True), node)
            ast.fix_missing_locations(trace)

            res.body = [trace] + [self.visit(i) for i in node.body]
            return res
        else:
            return node


def register_match_importer():
    sys.meta_path.insert(0, TranslatorImportHook(MatchStatementTranslator(), 'match-statement'))
