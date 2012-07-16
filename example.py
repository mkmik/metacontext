#- LANGUAGE match-statement -#

import inspect
from actor import match, case, _

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


class TestException(Exception):
    pass


def other_test(msg):
    def closure():
        with match(msg):
           with case ('test', _, _) as (a, b):
              print "CLOSURE LINE NR SHOULD BE 18", lineno()
              assert lineno() == 20
        pass
    closure()


def test(msg):
    with match(msg):
        with case ('test', _) as a:
            print "TEST", msg
            if False:
                print "A", a
            print "LINE NR SHOULD BE 27", lineno()
            assert lineno() == 32
        with case ('other', _):
            print "OTHER", msg
            raise TestException("let's look at the stack trace")


class MyActor(object):
    class Inner(object):
        def process(self, msg):
            with match(msg):
                with case('test', _):
                    assert lineno() == 43


    def run(self):
        msg = ('test', 1)
        with match(msg):
            with case ('test', _) as a:
                assert lineno() == 50
                print "wow"

        self.Inner().process(msg)

