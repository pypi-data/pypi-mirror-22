============
 z3c.bcrypt
============

z3c.bcrypt provides `zope.password`_ compatible "password manager" utilities
that use bcrypt (or alternatively pbkdf2) encoding for storing passwords.

Both encoding schemes are implemented in the cryptacular_ library that is
a dependency for this pacakge.

.. _`zope.password`: http://pypi.python.org/pypi/zope.password
.. _cryptacular: http://pypi.python.org/pypi/cryptacular


==================
 Using z3c.bcrypt
==================

    >>> from zope.interface.verify import verifyObject
    >>> from zope.password.interfaces import IPasswordManager
    >>> from z3c.bcrypt import BcryptPasswordManager
    >>> manager = BcryptPasswordManager()
    >>> verifyObject(IPasswordManager, manager)
    True

    >>> password = u"right \N{CYRILLIC CAPITAL LETTER A}"

    >>> encoded = manager.encodePassword(password)
    >>> encoded
    '$2a$...'
    >>> manager.checkPassword(encoded, password)
    True
    >>> manager.checkPassword(encoded, password + u"wrong")
    False

    >>> from z3c.bcrypt import PBKDF2PasswordManager
    >>> manager = PBKDF2PasswordManager()
    >>> verifyObject(IPasswordManager, manager)
    True

    >>> encoded = manager.encodePassword(password)
    >>> encoded
    u'$p5k2$...'
    >>> manager.checkPassword(encoded, password)
    True
    >>> manager.checkPassword(encoded, password + u"wrong")
    False

    >>> # A previously encoded password, should be decodable even if the
    >>> # current encoding of the same password is different::
    >>> previouslyencoded = (
    ...     '$p5k2$1000$LgAFPIlc9CgrlSaxHyTUMA='
    ...     '=$IuUYplhMkR4qCl8-ONRVjEgJNwE=')
    >>> encoded == previouslyencoded
    False
    >>> manager.checkPassword(previouslyencoded , password)
    True

Excessively long "passwords" will take up a lot of computation time that
can be used as a DOS attack vector. The password managers in z3c.bcrypt will
only use the first 4096 characters of the incoming password for checking.

This is inspired by:

  https://www.djangoproject.com/weblog/2013/sep/15/security/

This test would take significantly longer if the 4096 length limit would
not be in place. XXX how to test that reliably?

    >>> incomming = '$p5k2$1000$' + 'a' * 1024 * 1024 * 100  # lot of data.
    >>> manager.checkPassword(encoded, incomming)
    False

Configuration
=============

This package provides a ``configure.zcml`` which installs
implementations of the ``IPasswordManager`` as utilities:

    >>> from zope.configuration import xmlconfig
    >>> _ = xmlconfig.string("""
    ... <configure
    ...    xmlns="http://namespaces.zope.org/zope">
    ...
    ...    <include package="z3c.bcrypt" />
    ... </configure>
    ... """)

    >>> from zope import component
    >>> from zope.password.interfaces import IPasswordManager
    >>> component.getUtility(IPasswordManager, name='bcrypt')
    <z3c.bcrypt.passwordmanager.BcryptPasswordManager object at ...>
    >>> component.getUtility(IPasswordManager, name='pbkdf2')
    <z3c.bcrypt.passwordmanager.PBKDF2PasswordManager object at ...>


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




