import inspect
import new
import os
import sys
import tokenize


class TranslatorImportHook(object):

    def __init__(self, translator, tag):
        self.tag = tag
        self.translator = translator
        self.line_pos_patcher = LinePositionPatcher(self.translator.line_pos_offsets)

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
            translated = tokenize.untokenize(self.translator.translate(src.readline))
            line_pos_offsets = self.translator.line_pos_offsets

            print "Translated source:"
            print translated
            print "----------"
            print "line offsets", line_pos_offsets
            print "----------"

            compiled = compile(translated, self.src_name(fullname), 'exec', 0, True)
            exec compiled in m.__dict__

            self.line_pos_patcher.patch_line_numbers(m)

        return m


class LinePositionPatcher(object):

    def __init__(self, line_pos_offsets):
        self.line_pos_offsets = line_pos_offsets

    def patch_line_numbers(self, module):
        for k in dir(module):
            member = getattr(module, k)
            if inspect.isfunction(member):
                self.patch_function(member)
            elif inspect.isclass(member):
                self.patch_class(member)

    def patch_function(self, fun):
        fun.func_code = self.patch_code(fun.func_code)

    def patch_class(self, cls):
        for i in cls.__dict__.values():
            if inspect.isfunction(i):
                self.patch_function(i)
            if inspect.isclass(i):
                self.patch_class(i)

    def patch_code(self, code):
        """Creates a new code object with patched line position
        in it's co_lntab field, according to the line_pos_offsets map
        which is prepared during code translation

        The line_pos_offsets map contains the amount of lines which were inserted
        before a given line, so we just subtract this amount every time
        there is a line position information for a given statement.

        """
        firstlineno = code.co_firstlineno - sum([offset for line, offset in self.line_pos_offsets.items() if line < code.co_firstlineno])

        def patch(positions):
            for (op_pos, pos), (_, delta) in zip(absolutize(firstlineno, positions), positions):
                yield op_pos, delta - self.line_pos_offsets.get(pos, 0)

        consts = tuple(self.patch_code(c) if inspect.iscode(c) else c for c in code.co_consts)

        return self.clone_code(code, consts, firstlineno, pack(patch(unpack(code.co_lnotab))))

    def clone_code(self, c, consts, firstlineno, lnotab):
        return (new.code(c.co_argcount,c.co_nlocals,c.co_stacksize,c.co_flags,c.co_code,consts,c.co_names,c.co_varnames,c.co_filename,c.co_name,firstlineno,lnotab,c.co_freevars,c.co_cellvars))

    def print_lnotab(self, code, tab=None):
        if not tab:
            tab = code.co_lnotab

        for op_pos, line_nr in absolutize(code.co_firstlineno, unpack(tab)):
            print op_pos, line_nr


class Translator(object):
    def __init__(self):
        self.line_pos_offsets = {}

    op = {tokenize.NAME: 'NAME',
          tokenize.OP: 'OP',
          tokenize.INDENT: 'INDENT',
          tokenize.DEDENT: 'DEDENT',
          tokenize.NEWLINE: 'NEWLINE',
          tokenize.NL: 'NL',
          tokenize.COMMENT: 'COMMENT',
          }


class MatchStatementTranslator(Translator):
    def translate(self, readline):
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

            else:
                yield typ, name


def unpack(tab):
    """Unpack a code line number table from a coded byte array
    to a list of (op_delta, line_delta) pairs

    >>> unpack('\x01\x02\x03\x04')
    ... [(1, 2), (3, 4)]

    """
    def group(l, n):
        return zip(*(iter(l),) * n)

    return list(group([ord(i) for i in tab], 2))


def pack(unpacked):
    """Encode a list of (op_delta, line_delta) pairs into a byte array string
    suitable for storing in code.co_lntab:

    >>> pack([(1, 2), (3, 4)])
    ... '\x01\x02\x03\x04'

    """
    return ''.join(chr(i) for i in (item for sublist in unpacked for item in sublist))


def absolutize(firstlineno, unpacked):
    """Given a (unpacked) list of (op_pos, line_delta) pairs
    return a list of (op_pos, absolute_line_pos) pairs

    >>> list(absolutize(10, [(1, 2), (3, 4)]))
    ... [(1,12), (3, 16)]

    """
    line_nr = firstlineno

    for op, delta in unpacked:
        line_nr += delta
        yield op, line_nr


def register_match_importer():
    sys.meta_path.insert(0, TranslatorImportHook(MatchStatementTranslator(), 'match-statement'))
