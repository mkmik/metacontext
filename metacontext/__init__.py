import ast
import inspect
import importlib
import new
import os
import sys


class TranslatorImportHook(object):

    def __init__(self, tag=None):
        self.tag = tag

    def src_name(self, p, fullname):
        module_name = fullname.rsplit('.', 1)[-1]

        return os.path.join(p, '%s.py' % module_name)

    def find_module(self, fullname, path=None):
        if '.' in fullname:
            package_name, module_name = fullname.rsplit('.', 1)
        else:
            package_name, module_name = ('', fullname)

        package_path = ['']
        if package_name:
            package = importlib.import_module(package_name)
            package_path = package.__path__

        for p in package_path:
            loader = self.find_module_in_path(fullname, p)
            if loader:
                return loader

    def find_module_in_path(self, fullname, p):
        if os.path.exists(self.src_name(p, fullname)):
            # if the import hook was registered with a restriction tag,
            # we have to check if it's present in the file
            if self.tag:
                with open(self.src_name(p, fullname)) as f:
                    if f.readline().startswith('#- LANGUAGE %s -#' % self.tag):
                        return TranslatorLoader(p)
            # otherwise we just translate every single import
            else:
                return TranslatorLoader(p)
        return None

class TranslatorLoader(object):
    DEBUG = True
    #DEBUG = False

    def __init__(self, path):
        self.path = path

    def src_name(self, fullname):
        module_name = fullname.rsplit('.', 1)[-1]

        return os.path.join(self.path, '%s.py' % module_name)

    def load_module(self, fullname):
        print "Compiling module with match statement:", fullname
        m = new.module(fullname)
        m.__file__ = self.src_name(fullname)

        with open(self.src_name(fullname)) as src:
            tree = ast.parse(src.read(), self.src_name(fullname))
            known_keywords = self.parse_top_imports(tree)

            # transform only if we know about at least a keyword
            if True or known_keywords:
                translated = SyntaxTransformer(known_keywords).visit(tree)
                if self.DEBUG:
                    from metacontext.unparse import Unparser
                    print "-----"
                    Unparser(translated)
                    print "-----"
            else:
                translated = tree
            compiled = compile(translated, self.src_name(fullname), 'exec', 0, True)
            exec compiled in m.__dict__

        return m

    def parse_top_imports(self, tree):
        keywords = {}

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ImportFrom):
                mod = importlib.import_module(node.module)
                for alias in node.names:
                    name = alias.name
                    as_name = alias.asname or name

                    keyword = getattr(mod, name)
                    if inspect.isclass(keyword) and issubclass(keyword, Keyword):
                        keywords[as_name] = keyword()
                    elif isinstance(keyword, Keyword):
                        keywords[as_name] = keyword


        return keywords


class SyntaxTransformer(ast.NodeTransformer):
    def __init__(self, keywords):
        self.keywords = keywords
        self.stack = []
        self.gensym_counter = 0

    def gensym(self):
        self.gensym_counter += 1
        return "__g_%s" % self.gensym_counter

    def visit_With(self, node):

        try:
            self.stack.append({})

            if node.context_expr.func.id in self.keywords:

                keyword = self.keywords[node.context_expr.func.id]
                translated = keyword.translate(self, node.body, node.context_expr, node.optional_vars)

                if isinstance(translated, ast.AST):
                    translated = self.generic_visit(translated)

                    res = ast.copy_location(translated, node)
                    ast.fix_missing_locations(res)
                    return res
                else:
                    return [ast.copy_location(self.generic_visit(i), node) for i in translated]
            else:
                return self.generic_visit(node)

        finally:
            self.stack.pop()


class Keyword(object):
    pass


def register_importer_hook():
    sys.meta_path.insert(0, TranslatorImportHook('compile-time-context-manager'))
