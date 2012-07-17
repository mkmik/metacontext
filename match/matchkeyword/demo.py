#!/usr/bin/env python
def run():

    import metacontext
    metacontext.register_importer_hook()

    import dis
    import traceback

    import example

    try:
        example.test(('test', 1))
    except example.TestException:
        e = traceback.format_exc()
        print "GOT TRACEBACK", e
        assert 'line 35, in test' in e
        assert 'example.py' in e
        assert 'raise TestException("let\'s look at the stack trace")' in e

    example.other_test(('test', 1))

    example.MyActor().run()

    #print "---------"
    #dis.dis(example.test)


if __name__ == '__main__':
    run()
