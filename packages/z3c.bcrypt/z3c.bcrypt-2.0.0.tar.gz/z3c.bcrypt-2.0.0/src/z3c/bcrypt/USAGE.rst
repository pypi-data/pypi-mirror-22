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
