#- LANGUAGE match-statement -#

import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


class TestException(Exception):
    pass


def other_test(msg):
    match msg:
        case ('test', a):
            print "TEST", msg


def test(msg):
    match msg:
        case ('test', a):
            print "TEST", msg
            print "LINE NR SHOULD BE 24", lineno()
            assert lineno() == 25
        case ('other', a):
            print "OTHER", msg
            raise TestException("let's look at the stack trace")
