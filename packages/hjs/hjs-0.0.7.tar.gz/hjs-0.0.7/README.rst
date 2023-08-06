===
hjs 
===

``hjs`` is a thin wrapper around `hjson-py <http://github.com/hjson/hjson-py>`_

.. image:: https://duckduckgo.com/i/bf0eb228.png
.. code-block:: python

   >>> from hjs import hjs, dumps, loads, dump, load

   >>> da = hjs("""
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
   ...    value: 42
   ... }
   ... """)

   >>> assert da['value'] == 42
   >>> assert da.t.a == "you get the point, now :-)"

install as usual with ``pip install hjs``

Regards,
@CJC.

