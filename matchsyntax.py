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
            print "Translated source:"
            print translated
            print "----------"
            exec translated in m.__dict__

        return m

    def translate(self, readline):
        skip = 0
        for type, name, _, _, _ in tokenize.generate_tokens(readline):
            if type == tokenize.NAME and name == 'match':
                yield tokenize.NAME, 'if'
                yield tokenize.STRING, 'True'
                yield tokenize.OP, ':'
                skip = 2
            else:
                if skip > 0:
                    skip -= 1
                else:
                    yield type, name


def register_match_importer():
    sys.meta_path.insert(0, MatchStatementImportHook())
