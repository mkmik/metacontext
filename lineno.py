#!/usr/bin/env python

import dis
import inspect
import new

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def test():
    print "hello, from line", lineno()
    print "hello, again from line", lineno()


def clone_code(c, firstlineno, lnotab):
    return (new.code(c.co_argcount,c.co_nlocals,c.co_stacksize,c.co_flags,c.co_code,c.co_consts,c.co_names,c.co_varnames,c.co_filename,c.co_name,firstlineno,lnotab,c.co_freevars,c.co_cellvars))

def patch(f, line_mapping=dict()):
    tab = [i for i in f.func_code.co_lnotab]

    print "Line number table"
    print repr(''.join(tab))

    line_nr = f.func_code.co_firstlineno
    for op_pos, line_delta in zip((ord(tab[i]) for i in xrange(0, len(tab)-1, 2)), (ord(tab[i]) for i in xrange(1, len(tab), 2))):
        line_nr += line_delta
        print op_pos, line_nr

    print "----"

    for i, line_delta in ((i, ord(tab[i])) for i in xrange(1, len(tab), 2)):
        print 'IDX', line_delta
        tab[i] = chr(line_delta + 1)

    print repr(''.join(tab))

    print "Before patching"
    dis.disassemble(f.func_code)

    f.func_code = clone_code(f.func_code, f.func_code.co_firstlineno, ''.join(tab))

    print "After patching"
    dis.disassemble(f.func_code)

if __name__ == '__main__':
    test()
    patch(test)
    test()
