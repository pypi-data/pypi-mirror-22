Overview
========

OFSP registers the Zope 2 OFS content types.

Changelog
=========

4.0.1 (2017-06-11)
------------------

- Mark as compatible with Python 2 and 3.

4.0 (2016-07-23)
----------------

- Removed code from project, which got merged back into Zope2 itself.

3.0 (2016-07-19)
----------------

- Remove HelpSys support.

2.13.2 (2010-07-25)
-------------------

- Moved the registration of OFS types back into this packages `initialize`
  function to avoid test setup problems with installPackage in ZopeTestCase.

2.13.1 (2010-07-11)
-------------------

- Added a ``configure.zcml`` to automatically load the OFS package.

2.13.0 (2010-07-10)
-------------------

- Released as separate package.


