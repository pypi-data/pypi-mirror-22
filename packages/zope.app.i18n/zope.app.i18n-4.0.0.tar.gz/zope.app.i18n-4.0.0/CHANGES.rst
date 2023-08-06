=======
CHANGES
=======

4.0.0 (2017-05-25)
------------------

- Add support for Python 3.5, 3.6 and PyPy.

- Replace dependency on ``ZODB3`` with ``BTrees`` and ``persistent``.

- Drop test dependency on ``zope.app.testing``.

- The synchronization view now uses Python's built-in transport for
  handling Basic Authentication. As a reminder, Basic Authentication
  does not permit a colon (``:``) in the username, but does allow colons
  in the password (if the server properly conforms to the specification).

3.6.4 (2012-12-14)
------------------

- Fix translate() when used with ZODB 4.
- Remove test dependency on zope.app.component

3.6.3 (2010-09-01)
------------------

- Remove undeclared dependency on zope.deferredimport.
- Use zope.publisher >= 3.9 instead of zope.app.publisher.

3.6.2 (2009-10-07)
------------------

- Fix test_translate and follow recent change of HTTPResponse.redirect.

3.6.1 (2009-08-15)
------------------

- Added a missing testing dependency on zope.app.component.

3.6.0 (2009-03-18)
------------------

- Some of ZCML configuration was moved into another packages:

   * The global INegotiator utility registration was moved into ``zope.i18n``.
   * The include of ``zope.i18n.locales`` was also moved into ``zope.i18n``.
   * The registration of IModifiableUserPreferredLanguages adapter was moved
     into ``zope.app.publisher``.
   * The IAttributeAnnotation implementation statement for HTTPRequest was moved
     into ``zope.publisher`` and will only apply if ``zope.annotation`` is
     available.
   * The IUserPreferredCharsets adapter registration was also moved into
     ``zope.publisher``.

- Depend on zope.component >= 3.6 instead of zope.app.component as the
  ``queryNextUtility`` function was moved there.

- Remove the old ``zope.app.i18n.metadirectives`` module as the directive was
  moved to ``zope.i18n`` ages ago.

3.5.0 (2009-02-01)
------------------

- Use zope.container instead of zope.app.container.

3.4.6 (2009-01-27)
------------------

- Fix a simple inconsistent MRO problem in tests

- Substitute zope.app.zapi by direct calls to its wrapped apis. See bug
  219302.

3.4.5 (unreleased)
------------------

- This was skipped over by accident.

3.4.4 (2007-10-23)
------------------

- Fix deprecation warning.

3.4.3 (2007-10-23)
------------------

- Fix imports in tests.

- Clean up long lines.

3.4.2 (2007-9-26)
-----------------

- Release to fix packaging issues with 3.4.1.

3.4.1 (2007-9-25)
-----------------

- Added missing Changes.txt and README.txt files to egg

3.4.0 (2007-9-25)
-----------------

- Initial documented release

- Move ZopeMessageFactory to zope.i18nmessageid
