=========
 CHANGES
=========

4.1.0 (2017-05-25)
==================

- Raise the docutils ReST error report level from its default of
  ``error`` to ``severe``. An error-level report is issued for directives
  that are unknown, such as ``:class:``, which are increasingly common
  due to the use of Sphinx. This change prevents such an error being
  printed on stderr as well as rendered in the HTML.


4.0.0 (2017-05-17)
==================

- Add support for Python 3.4, 3.5, 3.6 and PyPy.

- Remove dependency on ``zope.app.testing``.

- Use the standard library ``doctest`` module.

3.5.1 (2009-07-21)
==================

- Require the new ``roman`` package, since docutils does not install it
  correctly.

3.5.0 (2009-01-17)
==================

- Adapted to docutils 0.5 for ReST rendering: get rid of the
  ZopeTranslator class, because docutils changed the way it
  uses translator so previous implementation doesn't work anymore.
  Instead, use publish_parts and join needed parts in the ``render``
  method of the renderer itself.

- Removed deprecated meta.zcml stuff and zpkg stuff.

- Replaced __used_for__ with zope.component.adapts calls.

3.4.0 (2007-10-27)
==================

- Initial release independent of the main Zope tree.
