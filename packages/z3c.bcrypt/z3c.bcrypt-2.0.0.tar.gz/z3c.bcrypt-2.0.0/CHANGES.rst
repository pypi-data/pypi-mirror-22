=========================
 Changelog of z3c.bcrypt
=========================

2.0.0 (2017-05-10)
==================

- Standardize namespace __init__.

- Add support for Python 3.4, 3.5, 3.6 and PyPy.


1.2 (2013-10-10)
================

- Only verify the first 4096 characters of a password to prevent
  denial-of-service attacks through repeated submission of large
  passwords, tying up server resources in the expensive computation
  of the corresponding hashes.

  See: https://www.djangoproject.com/weblog/2013/sep/15/security/

1.1 (2010-02-22)
================

- Fixes in the configure.zcml.

1.0 (2010-02-18)
================

- Initial public release.
