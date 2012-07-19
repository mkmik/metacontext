#- LANGUAGE compile-time-context-manager -#

import inspect
from matchkeyword.actor import match, case, _; from matchkeyword.actor import case as base

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


class TestException(Exception):
    pass


def other_test(msg):
    def closure():
        with match(msg):
           with case (('test', _, _)) as (a, b):
              print "CLOSURE LINE NR SHOULD BE 19", lineno()
              assert lineno() == 20
              assert (a, b) == (1, 2)
        pass
    closure()


def test(msg):
    with match(msg):
        with case (('test', _)) as a:
            print "TEST", msg
            if False:
                print "A", a
            print "LINE NR SHOULD BE 31", lineno()
            assert lineno() == 33
            print "OTHER", msg
            assert lineno() == 35
            raise TestException("let's look at the stack trace")


class MyActor(object):
    class Inner(object):
        def process(self, msg):
            with match(msg):
                with base(('test', _)):
                    raise TestException("Exception at line 43")
                with case(('other', _)):
                    raise TestException("Exception at line 45")


    def run(self):
        msg = ('test', 1)
        with match(msg):
            with case (('test', _)) as a:
                assert lineno() == 53
                print "wow", a

        self.Inner().process(msg)

def second_block(mesg):
    with match(mesg):
        with case(('other', _)):
            raise TestException("Exception at line 60")
        with case(('test', _)) as a:
            assert a == 1
            raise TestException("Exception at line 63")
