#- LANGUAGE match-statement -#

import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


class TestException(Exception):
    pass


def test(msg):
    match msg:
        case ('test', a):
            print "TEST", msg
            print "LINE NR SHOULD BE 18", lineno()
            assert lineno() == 19
        case ('other', a):
            print "OTHER", msg
            raise TestException("let's look at the stack trace")
