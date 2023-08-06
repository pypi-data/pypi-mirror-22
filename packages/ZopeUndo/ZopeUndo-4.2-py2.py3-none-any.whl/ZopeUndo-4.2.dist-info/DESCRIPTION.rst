Overview
========

This package is used to support the Prefix object that Zope 2 uses for the
undo log. It is a separate package only to aid configuration management.

This package is included in Zope 2. It can be used in a ZEO server to allow
it to support Zope 2's undo log , without pulling in all of Zope 2.


Changelog
=========

4.2 (2017-04-26)
----------------

- Add support for Python 3.6, drop support for Python 3.3.

4.1 (2016-04-03)
----------------

- Add compatibility with Python 3.4 and 3.5.

- Drop support for Python 2.6 and 3.2.

4.0 (2013-03-02)
----------------

- Add compatibility with Python 3.2 and 3.3. Note that the Prefix class
  only provides equality testing, but doesn't support ordering.

2.12.0 (2010-04-05)
-------------------

- Released as separate package.


