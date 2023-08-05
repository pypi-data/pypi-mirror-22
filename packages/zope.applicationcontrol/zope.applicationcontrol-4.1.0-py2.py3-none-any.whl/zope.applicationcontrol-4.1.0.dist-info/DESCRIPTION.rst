``zope.applicationcontrol``
===========================

.. image:: https://travis-ci.org/zopefoundation/zope.applicationcontrol.png?branch=master
        :target: https://travis-ci.org/zopefoundation/zope.applicationcontrol

The application control instance can be generated upon startup of an
application built with the Zope Toolkit.

This package provides an API to retrieve runtime information. It also
provides a utility with methods for shutting down and restarting the
server.


Changes
=======

4.1.0 (2017-05-03)
------------------

- Add support for Python 3.5 and 3.6.

- Drop support for Python 3.2 and 2.6.


4.0.1 (2015-06-05)
------------------

- Add support for Python 3.2 and PyPy3.


4.0.0 (2014-12-24)
------------------

- Add support for PyPy.  (PyPy3 is pending release of a fix for:
  https://bitbucket.org/pypy/pypy/issue/1946)

- Add support for Python 3.4.

- Add support for testing on Travis.


4.0.0a1 (2013-02-22)
--------------------

- Add support for Python 3.3.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.


3.5.5 (2010-01-09)
------------------

- Initial release, extracted from ``zope.app.applicationcontrol``.


