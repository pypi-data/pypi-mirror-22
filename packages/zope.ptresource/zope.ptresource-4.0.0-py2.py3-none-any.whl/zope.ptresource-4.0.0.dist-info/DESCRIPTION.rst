``zope.ptresource`` Overview
============================

.. note::

   This package is at present not reusable without depending on a large
   chunk of the Zope Toolkit and its assumptions. It is maintained by the
   `Zope Toolkit project <http://docs.zope.org/zopetoolkit/>`_.

This package provides a "page template" resource class, a resource which
content is processed with Zope Page Templates engine before returning to
client.

The resource factory class is registered for "pt", "zpt" and "html" file
extensions in package's ``configure.zcml`` file.


Changes
=======

4.0.0 (2014-12-24)
==================

- Add support for PyPy and PyPy3.

- Add support for Python 3.4.

- Add support for testing on Travis.


4.0.0a1 (2013-02-25)
====================

- Add support for Python 3.3.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.


3.9.0 (2009-08-27)
==================

Initial release. This package was splitted off zope.app.publisher as a part
of refactoring process. It's now a plugin for another package that was
refactored from zope.app.publisher - zope.browserresource. See its
documentation for more details.

Other changes:

 * Don't render PageTemplateResource when called as the IResource interface
   requires that __call__ method should return an absolute URL. When accessed
   by browser, it still will be rendered, because "browserDefault" method now
   returns a callable that will render the template to browser.


