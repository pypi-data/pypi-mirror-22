SyntaxDB
========

This is a small Python library for accessing the
`SyntaxDB <https://syntaxdb.com/>`__ API.

`SyntaxDB <https://syntaxdb.com/>`__ is a programing language syntax
database. See https://syntaxdb.com/about for more infomation.

Official documentation of the API can be found at
https://syntaxdb.com/api/v1.

Installation
------------

::

    pip install syntaxdb

Usage
-----

.. code:: python

    import syntaxdb

Authentication
--------------

Authentication is not required for the usage of the API.

Queries
-------

First is an example:

.. code:: python

    import syntadb

    db = syntaxdb.syntaxdb()

    #add parameters if neccessary:
    db.parameters['language_permalink'] = 'python'

    #query concepts of language (here is Python):
    db.concept()

Before executing some queries, we need to add the parameters (if
neccessary).

.. code:: python

    db.parameters['parameter_name'] = value

Then call ``concept()``, ``language()``, ``category()`` to get what we
want (in the example we get all concepts corresponding to Python).

After finishing query, we can change parameters to make another query.

See parameters list in API's document: https://syntaxdb.com/api/v1.

More detail about operations, parameter's type, required parameters,
response content type ... can be found at the API documentation too.

To query an operation(listed in the API doc), we just simple add exactly
parameters mentioned in the doc (pay attention to required parameters),
then call ``concept()``, ``language()`` or ``category()``.

Contributing
------------

Bug reports and pull requests are welcome at
https://github.com/lhat-messorem/syntax\_db.

License
-------

This library is a open source software licensed under the `MIT
License <http://opensource.org/licenses/MIT>`__. Details provided in the
LICENSE file.

SyntaxDB API copyrights © 2017 SyntaxDB
