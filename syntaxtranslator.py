import ast
import new
import os
import sys


class TranslatorImportHook(object):

    def __init__(self, tag):
        self.tag = tag

    def src_name(self, fullname):
        return '%s.py' % fullname

    def find_module(self, fullname, path=None):
        if os.path.exists(self.src_name(fullname)):
            with open(self.src_name(fullname)) as f:
                if f.readline().startswith('#- LANGUAGE %s -#' % self.tag):
                    return self
        return None

    def load_module(self, fullname):
        print "Compiling module with match statement:", fullname
        m = new.module(fullname)
        m.__file__ = self.src_name(fullname)

        with open(self.src_name(fullname)) as src:
            tree = ast.parse(src.read(), self.src_name(fullname))
            known_keywords = self.parse_top_imports(tree)
            translated = SyntaxTransformer(known_keywords).visit(tree)
            compiled = compile(translated, self.src_name(fullname), 'exec', 0, True)
            exec compiled in m.__dict__

        return m

    def parse_top_imports(self, tree):
        from matchsyntax import match, case

        return {'match': match(), 'case': case()}


class SyntaxTransformer(ast.NodeTransformer):
    def __init__(self, keywords):
        self.keywords = keywords

    def visit_With(self, node):

        node = self.generic_visit(node)

        if node.context_expr.func.id in self.keywords:
            keyword = self.keywords[node.context_expr.func.id]
            res = ast.copy_location(keyword.translate(node.body, node.context_expr, node.optional_vars), node)
            ast.fix_missing_locations(res)
            res.body = [self.visit(i) for i in node.body]
            return res
        else:
            return node


class Keyword(object):
    pass


def register_translator_importer():
    sys.meta_path.insert(0, TranslatorImportHook('compile-time-context-manager'))
