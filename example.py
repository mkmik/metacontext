#- LANGUAGE match-statement -#

import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


class TestException(Exception):
    pass


def other_test(msg):
    def closure():
        match msg:
           case ('test', a):
              print "CLOSURE LINE NR SHOULD BE 18", lineno()
              assert lineno() == 19
    closure()


def test(msg):
    match msg:
        case ('test', a):
            print "TEST", msg
            print "LINE NR SHOULD BE 27", lineno()
            assert lineno() == 28
        case ('other', a):
            print "OTHER", msg
            raise TestException("let's look at the stack trace")


class MyActor(object):
    def run(self):
        msg = ('test', 1)
        match msg:
            case ('test', a):
                assert lineno() == 39
