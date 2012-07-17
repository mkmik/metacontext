import ast
import inspect
import new
import os


class TranslatorImportHook(object):

    def __init__(self, translator, tag):
        self.tag = tag
        self.translator = translator

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
            translated = self.translator.translate(tree)
            compiled = compile(translated, self.src_name(fullname), 'exec', 0, True)
            exec compiled in m.__dict__

        return m


class Translator(object):
    def __init__(self):
        pass
