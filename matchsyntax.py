import new
import os
import sys
import tokenize


class MatchStatementImportHook(object):

    def src_name(self, fullname):
        return '%s.py' % fullname

    def find_module(self, fullname, path=None):
        if os.path.exists(self.src_name(fullname)):
            with open(self.src_name(fullname)) as f:
                if f.readline().startswith('#- LANGUAGE match-statement -#'):
                    return self
        return None

    def load_module(self, fullname):
        print "Compiling module with match statement:", fullname
        m = new.module(fullname)

        with open(self.src_name(fullname)) as src:
            translated = tokenize.untokenize(self.translate(src.readline))
            exec translated in m.__dict__

        return m

    def translate(self, readline):
        for type, name, _, _, _ in tokenize.generate_tokens(readline):
            yield type, name


def register_match_importer():
    sys.meta_path.insert(0, MatchStatementImportHook())
