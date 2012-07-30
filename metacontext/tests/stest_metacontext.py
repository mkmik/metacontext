#- LANGUAGE compile-time-context-manager -#

from metacontext.tests.testcontext import timeit
from metacontext.tests.utils import intercept_stdout

def stest_it():
    with timeit(log=True) as took:
        print "Logged"

    assert took >= 0

    with intercept_stdout() as msg:
        with timeit() as took:
            print "Not logged"

    assert took >= 0
    assert msg.getvalue() == "Not logged\n"

    dolog = False

    with intercept_stdout() as msg:
        with timeit(log=dolog) as took:
            print "Not logged"

    assert took >= 0
    assert msg.getvalue() == "Not logged\n"
