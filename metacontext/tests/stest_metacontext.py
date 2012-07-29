#- LANGUAGE compile-time-context-manager -#

from metacontext.tests.testcontext import timeit

def stest_it():
    print "testIIIIIIIIIIIIIIING"
    with timeit():
        print "TIMED"
