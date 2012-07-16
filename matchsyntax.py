import sys
import token
import tokenize

from syntaxtranslator import Translator, TranslatorImportHook


class MatchStatementTranslator(Translator):
    def translate(self, readline):
        tokens = tokenize.generate_tokens(readline)

        ANY = object()

        def until(typ, name):
            for t, n, _, _, _ in tokens:
                if t == typ and (name == ANY or n == name):
                    return n

        buffer = []

        is_bol = True
        in_with = False
        for typ, name, start_pos, _, _ in tokens:
            print "GOT: %s(%s) (in with: %s)" % (token.tok_name.get(typ, typ), repr(name), in_with)

            if in_with and typ == tokenize.NAME and name == 'match':
                yield tokenize.NAME, 'if'
                yield tokenize.STRING, 'True'
                yield tokenize.OP, ':'

                until(tokenize.OP, ':')

                buffer = []
            elif in_with and typ == tokenize.NAME and name == 'case':
                yield tokenize.NAME, 'if'
                yield tokenize.STRING, 'True'
                yield tokenize.OP, ':'

                # doesn't handle "case ....: statement1; statement2;"
                indent = until(tokenize.INDENT, ANY)

                yield tokenize.NL, '\n'
                yield tokenize.INDENT, indent

                # shift user's statement positions by 1
                # the user's statement is 2 lines ahead of the case
                # because we inserted 1 trace statement
                self.line_pos_offsets[start_pos[0] + 2] = 1

                yield tokenize.NAME, 'print'
                yield tokenize.String, '"fun trace line: %s"' % (start_pos[0]+1)
                yield tokenize.NL, '\n'

                buffer = []
            else:
                if is_bol and typ == tokenize.NAME and name == 'with':
                    buffer.append((typ, name))
                else:
                    for t, n in buffer:
                        yield t, n
                    buffer = []
                    yield typ, name

            in_with = is_bol and typ == tokenize.NAME and name == 'with'
            is_bol = typ == tokenize.NEWLINE or typ == tokenize.INDENT or typ == tokenize.DEDENT

def register_match_importer():
    sys.meta_path.insert(0, TranslatorImportHook(MatchStatementTranslator(), 'match-statement'))
