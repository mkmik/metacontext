#!/usr/bin/env python
def run():

    import metacontext
    metacontext.register_importer_hook()

    import dis
    import traceback

    import example

    try:
        try:
            example.test(('test', 1))
        except example.TestException:
            e = traceback.format_exc()
            print "GOT TRACEBACK", e
            assert 'line 37, in test' in e
            assert 'example.py' in e
            assert 'raise TestException("let\'s look at the stack trace")' in e

        example.other_test(('test', 1, 2))

        try:
            example.MyActor().run()
        except example.TestException:
            e = traceback.format_exc()
            print "GOT SECOND TRACEBACK", e

        try:
            example.second_block(('test', 1))
        except example.TestException:
            e = traceback.format_exc()
            print "GOT THIRD TRACEBACK", e

    finally:
        print "---------"
        print "X", repr(example.second_block.func_code.co_lnotab)
        dis.dis(example.second_block)


if __name__ == '__main__':
    run()
