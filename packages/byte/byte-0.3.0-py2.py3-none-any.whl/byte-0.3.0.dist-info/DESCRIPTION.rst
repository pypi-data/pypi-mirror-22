byte
====

.. image:: https://img.shields.io/pypi/v/byte.svg?style=flat-square
   :target: https://pypi.python.org/pypi/byte

.. image:: https://img.shields.io/travis/fuzeman/byte.svg?style=flat-square
   :target: https://travis-ci.org/fuzeman/byte

.. image:: https://img.shields.io/codeclimate/github/fuzeman/byte.svg?style=flat-square
   :target: https://codeclimate.com/github/fuzeman/byte

.. image:: https://img.shields.io/coveralls/fuzeman/byte/master.svg?style=flat-square
   :target: https://coveralls.io/github/fuzeman/byte

Modular data-model framework, and object-relational mapper.

**Supported Platforms:**

- **Python:** 2.6, 2.7, 3.3+
- **PyPy 2:** 2.5+
- **PyPy 3:** 5.5+

**Requirements:**

- **Arrow:** 0.10.0+
- **PyParsing:** 2.2.0+
- **Six:** 1.10.0+

Development
-----------

**Status:** Alpha

Usable, but many features are still in development.

**Planned for Beta:**

- Database/Table Support
- Reduce requirements:

  - Create an alternate fallback datetime translator *(arrow)*
  - Move the expression parser to an optional plugin package *(pyparsing)*

- Joins:

  - JOIN
  - LEFT JOIN
  - LEFT OUTER JOIN
  - INNER JOIN
  - CROSS JOIN

- Queries:

  - DELETE
  - INSERT (SELECT ...)
  - INSERT OR [REPLACE, ROLLBACK, ABORT, FAIL, IGNORE]
  - UPDATE
  - UPDATE OR [ROLLBACK, ABORT, REPLACE, FAIL, IGNORE]

Plugins
-------

**Compilers:**

- `byte-sqlite <https://github.com/fuzeman/byte-sqlite>`_ *(alpha)*

**Executors:**

- `byte-apsw <https://github.com/fuzeman/byte-apsw>`_ *(alpha)*
- `byte-sqlite <https://github.com/fuzeman/byte-sqlite>`_ *(alpha)*
- `byte-pysqlite <https://github.com/fuzeman/byte-pysqlite>`_ *(alpha)*

**Formats:**

- `byte-ijson <https://github.com/fuzeman/byte-ijson>`_ *(alpha)*
- `byte-msgpack <https://github.com/fuzeman/byte-msgpack>`_ *(alpha)*



