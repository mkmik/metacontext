MetaContext
===========

It's always been possible to write domain specific languages in python, but it's rigid syntax, the lack of smalltalk like "blocks"
(or at least anonymous closures which can contain statements) make it hard, if not impossible, to design slick DSL.

This library provides a powerful language extension mechanism that tries to follow the python language design principles
and avoid creating confusing syntax constructs that will break compatibilities with editor extensions such as emacs flymake.

With MetaContext you can define macros which can manipulate the AST of it's body and inject abitrary code.

Example
-------

Imagine you want to build a pattern matching construct. Without MetaContext you could design the DSL like this::

  with pattern_match(msg) as case:

    @case(('something', ANY))
    def _(value):
       do_something_with(value)

    @case(('error', ANY))
    def _(e):
       handle_error(e)


The `pattern_match` context manager can check if at least one case has been executed and raise a `NoMatch` exception
otherwise.

However this DSL has two problems:

  1. It's more verbose than necessary
  2. It requires the case mangers to be contained in closures which cannot break out of loops, perform (non local) returns,
     yield out of a generator etc.

With MetaContext you can define the DSL as::

  with pattern_match(msg):
    with case(('something', ANY)) as value:
       do_something_with(value)
    with case(('error', ANY)) as e:
       handle_error(e)

This construct will allow you to interact nicely with generator based coroutines (like twisted inline callbacks)::

  with pattern_match(msg):
    with case(('something', ANY)) as value:
       res = yield do_something_with(value)
       do_something_else(res)
    with case(('error', ANY)) as e:
       handle_error(e)

Or perform returns::

  with pattern_match(msg):
    with case(('something', ANY)) as value:
       res = do_something_with(value)
       if is_it_the_correct_one(res):
         return
    with case(ANY):
       pass


Another possible use case is retryng a body in case of exceptions::

  with retry(IOException):
    do_something()
    do_something_else()

Which would have been written as::

  while True:
    try:
      do_something()
      do_something_else()
    except IOException:
      pass
    else:
      break

How to create your own meta context mangers
--------------------------------------------

Just create a `Keyword` subclass::

  class retry(Keyword):
     def __init__(self, *excs):
        self.exceptions = excs

     def transform(self, translator, body, args, var):
        # ... return a transformed python AST object
        # you will get the `with` body in `body`


How to use your meta context manger
------------------------------------

If you want to use your meta context manger, you first have to register
the MetaContext import hook::

  import metacontext
  metacontext.register_importer_hook()

Then every source file that imports a symbol that resolves to a subclass of `Keyword` will
be intercepted by the import hook and it's AST will be given to the meta context mangers
which will usually transform the body of the `with` statement::

  from yourpackage.retrymanger import retry

  # ...

  with retry():
    # ....


Macro definition language
-------------------------

Maniuplating the AST directly is a verbose and cumbersome process, especially since
you have to care about preserving original line number information for debugging and stack trace purposes.

MetaContext offers a macro definition DSL that you can use to quickly create your own meta context mangers:

The macro definition DSL itself is built using MetaContext constructs::

  class retry(Keyword):
     def __init__(self, *excs):
        self.exceptions = excs

     def template(self, translator, body, args, var):
        with quote() as q:
          while True:
            try:
              unquote_stmts(body)
            except IOException:
              pass
            else:
              break

        return q

The MetaContext library will do it's best to preserve the original line number of the unquoted statements
so that you can seamlessly use your constructs in your sources as if they were native python.

Notes
-----

Currently, since the library is in development, the modules which you want to transform with MetaContext have to
contain this line as the first line of their source::

  #- LANGUAGE compile-time-context-manager -#

This restriction will be lifted as soon as we make sure we can correctly handle all the import hook rough edges.
