wikitables
==========

|Documentation Status| |PyPI version|

Import tables from any Wikipedia article as a dataset in Python

Installing
----------

.. code:: bash

    pip install wikitables

Usage
-----

Importing
~~~~~~~~~

Importing all tables from a given article:

.. code:: python

    from wikitables import import_tables
    tables = import_tables('List of cities in Italy') #returns a list of WikiTable objects

To import an article from a different language, simply add the Wikipedia
language code as an argument to ``import_tables``

.. code:: python

    tables = import_tables('İtalya\'daki_şehirler_listesi', 'tr') #returns a list of WikiTable objects

Accessing
~~~~~~~~~

Iterate over a table's rows:

.. code:: python

    print(tables[0].name)
    for row in tables[0].rows:
        print('{City}: {Area(km2)}'.format(**row))

output:

::

    List of cities in Italy[0]
    Milan: 4,450.11
    Naples: 3,116.52
    Rome: 3,340.41
    Turin: 1,328.40
    ...

Or return the table encoded as JSON:

.. code:: python

    tables[0].json()

output:

.. code:: json

    [
        {
            "City": "Milan",
            "Population January 1, 2014": "6,623,798",
            "Density(inh./km2)": "1,488",
            "Area(km2)": "4,450.11"
        },
        {
            "City": "Naples",
            "Population January 1, 2014": "5,294,546",
            "Density(inh./km2)": "1,699",
            "Area(km2)": "3,116.52"
        },
        ...

Table Head
~~~~~~~~~~

After import, table column names may been modified by setting a new
header:

.. code:: python

    table.head = [ 'newfield1', 'newfield2', 'newfield3' ]

This change will be recursively reflected on all of a given tables rows.

Roadmap
-------

Some planned and wishlist features:

-  Type guesing from MediaWiki template values

.. |Documentation Status| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
   :target: http://wikitables.readthedocs.org/en/latest
.. |PyPI version| image:: https://badge.fury.io/py/wikitables.svg
   :target: https://badge.fury.io/py/wikitables
