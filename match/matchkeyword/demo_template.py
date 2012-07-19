#!/usr/bin/env python
def run():

    import metacontext
    metacontext.register_importer_hook()

    import dis

    from matchkeyword import matchsyntax

    try:
        pass
    finally:
        print "---------"
        dis.dis(matchsyntax.case.template)

        from metacontext.unparse import Unparser

        template_ast = matchsyntax.case.template(None, None, None, None)
        print template_ast
        Unparser(template_ast)


if __name__ == '__main__':
    run()
