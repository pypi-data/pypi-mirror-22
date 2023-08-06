Argpar
======

A simple argument parser.

Usage
-----

.. code:: python

    import argpar
    import copy
    opts = {"o": None, "g": "foo", "w": None}
    flags = ["t", "u"]
    posarg = {"path": "/home"}
    argpar.parse(opts, flags, {}, copy.copy(sys.argv))

Vaules in ``opts`` and ``posarg`` dictionaries are default values.

Will automaticaly print help message if a ``h`` flag is found and exit.

We recomend copying ``sys.argv``, as arguments get removed during
parsing.
