``zope.size``
=============

.. image:: https://travis-ci.org/zopefoundation/zope.size.png?branch=master
        :target: https://travis-ci.org/zopefoundation/zope.size

This package provides a definition of simple interface that allows
applications to retrieve the size of the object for displaying and for sorting.

The default adapter is also provided. It expects objects to have the ``getSize``
method that returns size in bytes.  However, the adapter won't crash if an
object doesn't have one and will show size as "not available" instead.


Changes
=======

4.1.0 (2014-12-29)
------------------

- Add support for PyPy3.

- Add support for Python 3.4.

- Add support for testing on Travis.


4.0.1 (2013-03-08)
------------------

- Add Trove classifiers indicating CPython and PyPy support.


4.0.0 (2013-02-13)
------------------

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.

- Add support for Python 3.2 and 3.3.

- Conditionally disable tests that require ``zope.configuration`` and 
  ``zope.security``.


3.5.0 (2011-11-29)
------------------

- Include zcml dependencies in configure.zcml, require the necessary packages
  via a zcml extra, added tests for zcml.

3.4.1 (2009-09-10)
------------------

- Add support for bootstrapping on Jython.

- Add docstrings.

- Beautify package's README and include CHANGES into the description.

- Change package's url to PyPI instead of Subversion.

3.4.0 (2006-09-29)
------------------

- First release as a separate egg


