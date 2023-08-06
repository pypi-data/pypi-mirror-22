===
hjs
===


.. module:: hjs


``hjs`` is a thin wrapper around `hjson <http://github.com/hjson/hjson-py>`_

.. image:: https://duckduckgo.com/i/bf0eb228.png
.. code-block:: python

   >>> from hjs import hjs, dumps, loads, dump, load

   >>> da = loads("""
   ... {
   ...    a: 1
   ...    b: are you ok with it ?
   ...    c: '''
   ...       what a rest,
   ...       isn't it ?
   ...       '''
   ...    t: {
   ...        a: you get the point, now :-)
   ...    },
   ...    values: 42
   ... }
   ... """)

   >>> assert da['values'] == 42
   >>> assert da.t.a == "you get the point, now :-)"

You can find further information (installation instructions, mailing list)
as well as the source code and issue tracker on our
`GitHub page <https://github.com/charbeljc/hjs/>`__.

_(actually not, you're reading the whole doc, just `pip install hjs` and you are done.)_
