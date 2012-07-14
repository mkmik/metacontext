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
            line_pos_offsets = {}
            translated = tokenize.untokenize(self.translate(src.readline, line_pos_offsets))
            print "Translated source:"
            print translated
            print "----------"
            print "line offsets", line_pos_offsets
            print "----------"
            exec translated in m.__dict__

        return m

    op = {tokenize.NAME: 'NAME',
          tokenize.OP: 'OP',
          tokenize.INDENT: 'INDENT',
          tokenize.DEDENT: 'DEDENT',
          tokenize.NEWLINE: 'NEWLINE',
          tokenize.NL: 'NL',
          tokenize.COMMENT: 'COMMENT',
          }

    def translate(self, readline, line_pos_offsets):
        tokens = tokenize.generate_tokens(readline)

        ANY = object()

        def until(typ, name):
            for t, n, _, _, _ in tokens:
                if t == typ and (name == ANY or n == name):
                    return n

        for typ, name, start_pos, _, _ in tokens:
            print "GOT: %s(%s)" % (self.op.get(typ, typ), repr(name))

            if typ == tokenize.NAME and name == 'match':
                yield tokenize.NAME, 'if'
                yield tokenize.STRING, 'True'
                yield tokenize.OP, ':'

                until(tokenize.OP, ':')
            elif typ == tokenize.NAME and name == 'case':
                yield tokenize.NAME, 'if'
                yield tokenize.STRING, 'True'
                yield tokenize.OP, ':'

                until(tokenize.OP, ':')
            else:
                yield typ, name


def register_match_importer():
    sys.meta_path.insert(0, MatchStatementImportHook())
