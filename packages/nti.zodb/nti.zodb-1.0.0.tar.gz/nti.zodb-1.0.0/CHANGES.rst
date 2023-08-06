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
