=========
 CHANGES
=========

1.0.0 (2017-05-10)
==================

- Add support for Python 3.4, 3.5, 3.6 and PyPy.

- Fix typo in Dutch translation


0.11 (2011-06-28)
=================

- Added nl translations.


0.10 (2011-02-08)
=================

- Exception views do not by default provide ISystemErrorView anymore as it
  would result in duplicate log output. The mixin class still exists for
  writing custom error views that do provide ISystemErrorView.

0.9 (2011-01-20)
================

- Initial release.
