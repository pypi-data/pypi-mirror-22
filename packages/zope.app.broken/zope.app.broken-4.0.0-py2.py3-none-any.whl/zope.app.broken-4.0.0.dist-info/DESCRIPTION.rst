When an object cannot be correctly loaded from the ZODB, this package allows
this object still to be instantiated, but as a "Broken" object. This allows
for gracefully updating the database without interuption.


=========
 CHANGES
=========

4.0.0 (2017-05-16)
==================

- Add support for Python 3.4, 3.5, 3.6 and PyPy.

- Change dependency on ``ZODB3`` to ``ZODB``.

- The ``browser.zcml`` will only be loaded if ``zope.browserpage`` is
  installed.

- Accessing the ``__parent__`` and ``__name__`` attributes of broken
  objects will no longer raise ``AttributeError`` if the state is an
  unexpected type, instead returning ``None``.


3.6.0 (2010-09-25)
==================

- Depend on new ``zope.processlifetime`` interfaces and implementations
  instead of using BBB imports from ``zope.app.appsetup``.

- Added test extra to declare test dependency on ``zope.testing``.

- Using Python's ``doctest`` module instead of depreacted
  ``zope.testing.doctest``.


3.5.0 (2009-02-05)
==================

- Depend on new ``zope.broken`` package for the ``IBroken`` interface.

3.4.0 (2007-10-11)
==================

- Initial release independent of the main Zope tree.


