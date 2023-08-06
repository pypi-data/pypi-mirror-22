localimport
===========

– Isolated import of Python modules

Features
--------

-  emulates a partly isolated environment for local modules
-  evaluates ``*.pth`` files
-  supports ``pkg_resources`` namespaces
-  mocks ``pkgutil.extend_path()`` to support zipped Python eggs

Example
-------

Given your Python script, application or plugin comes with a directory
that contains modules for import, you can use localimport to keep the
global importer state clean.

::

    app.py
    res/modules/
      some_package/
        __init__.py

.. code:: python

    # app.py
    with localimport('res/modules') as _importer:
        import some_package
    assert 'some_package' not in sys.modules

    **Note**: It is very important that you keep the reference to the
    ``localimport`` object alive, especially if you use
    ``from xx import yy`` imports.

Use with `require <https://github.com/NiklasRosenstein/py-require>`__
---------------------------------------------------------------------

The ``localimport`` class is defines as ``exports`` symbols, thus when
you ``require()`` the module, what you get is the class directly rather
then the module.

.. code:: python

    import require
    localimport = require('./localimport')

    with localimport('res/modules') as _importer:
      # ...

Building a minified version
---------------------------

In many cases it doesn't make much sense to use localimport as yet
another Python package, thus you might want to include an inlined and
minified version of it into your codebase. For this you can use either
`pyminifier <https://pypi.python.org/pypi/pyminifier>`__ or
`py-blobbify <https://pypi.python.org/pypi/py-blobbify>`__ depending on
what format you want to include into your code.

::

    $ pyminifier localimport.py
    $ py-blobbify localimport.py --export-symbol=localimport -mc

You can find pre-minified versions
`here <http://bitly.com/localimport-min>`__.

Changelog
---------

v1.5.2
~~~~~~

-  fix #17 where ``sys.modules`` changed size during iteration in
   ``localimport.__enter__()`` (Python 3)

v1.5.1
~~~~~~

-  add Python 3 compatibility

v1.5
~~~~

-  add ``setup.py``
-  add ``make_min`` and ``make_b64`` commands to ``setup.py``
-  fix possible error when ``localimport(parent_dir)`` parameter is not
   specified and the ``__file__`` of the Python module that uses
   localimport is in the current working directory

v1.4.16
~~~~~~~

-  fix possible ``KeyError`` when restoring namespace module paths
-  renamed ``_localimport`` class to ``localimport``
-  ``localimport(parent_dir)`` parameter is now determined dynamically
   using ``sys._getframe()``
-  support for
   `py-require <https://github.com/NiklasRosenstein/py-require>`__

v1.4.14
~~~~~~~

-  Mockup ``pkg_resources.declare_namespace()``, making it call
   ``pkgutil.extend_path()`` afterwards to ensure we find all available
   namespace paths

v1.4.13
~~~~~~~

-  fixed possible KeyError and AttributeError when using the
   ``_localimport.disable()`` method

v1.4.12
~~~~~~~

-  Removed auto discovering of modules importable from the local site
-  Add ``_localimport.disable()`` method

v1.4.11
~~~~~~~

-  Fixed a bug where re-using the ``_localimport`` context added local
   modules back to ``sys.modules`` but removed them immediately (#15)

v1.4.10
~~~~~~~

-  Fix #13, ``_extend_path()`` now keeps order of the paths
-  Updat class docstrings
-  Add ``do_eggs`` and ``do_pth`` parameters to the constructor
-  Fix #12, add ``_discover()`` method and automatic disabling of
   modules that could conflict with modules from the ``_localimport``
   site

v1.4.9
~~~~~~

-  Fix #11, remove ``None``-entries of namespace packages in
   ``sys.modules``
-  ``_localimport._extend_path()`` is is now less tolerant about
   extending the namespace path and only does so when a
   ``__init__.{py,pyc,pyo}`` file exists in the parsed directory

v1.4.8
~~~~~~

-  Now checks any path for being a zipfile rather than just .egg files

License
-------

The MIT License (MIT)

Copyright (c) 2015-2016 Niklas Rosenstein

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
