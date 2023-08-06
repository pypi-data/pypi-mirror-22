==========
 nti.zodb
==========

.. image:: https://travis-ci.org/NextThought/nti.zodb.svg?branch=master
    :target: https://travis-ci.org/NextThought/nti.zodb

.. image:: https://coveralls.io/repos/github/NextThought/nti.zodb/badge.svg?branch=master
    :target: https://coveralls.io/github/NextThought/nti.zodb?branch=master

.. image:: https://readthedocs.org/projects/ntizodb/badge/?version=latest
    :target: http://ntizodb.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Utilities for working with ZODB.

Complete documents are found at http://ntizodb.readthedocs.io/


=========
 Changes
=========


1.0.0 (2017-06-08)
==================

- First PyPI release.
- Add support for Python 3.
- Remove nti.zodb.common. See
  https://github.com/NextThought/nti.zodb/issues/1.
  ``ZlibClientStorageURIResolver`` will no longer try to set a ``var``
  directory to store persistent cache files automatically.
- ``CopyingWeakRef`` now implements ``ICachingWeakRef``.


