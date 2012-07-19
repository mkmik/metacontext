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

        import ast
        body = ast.parse("print 'hello'").body
        template_ast = matchsyntax.case.template(1, body, 2, 3)
        print template_ast
        Unparser(template_ast)


if __name__ == '__main__':
    run()
