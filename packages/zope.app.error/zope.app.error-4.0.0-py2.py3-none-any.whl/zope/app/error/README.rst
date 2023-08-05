======
README
======

This package provides an error reporting utility which is able to
store errors. (Notice that the implementation classes have been moved
to the ``zope.error`` package.)

Let's create one:

  >>> from zope.app.error.error import ErrorReportingUtility
  >>> util = ErrorReportingUtility()
  >>> util
  <zope.error.error.ErrorReportingUtility object at ...>

  >>> from zope.app.error.interfaces import IErrorReportingUtility
  >>> IErrorReportingUtility.providedBy(util)
  True
  >>> IErrorReportingUtility
  <InterfaceClass zope.error.interfaces.IErrorReportingUtility>

This package contains ZMI views in the ``browser`` sub-package:

  >>> from zope.app.error.browser import EditErrorLog, ErrorRedirect
  >>> EditErrorLog
  <class 'zope.app.error.browser.EditErrorLog'>
  >>> ErrorRedirect
  <class 'zope.app.error.browser.ErrorRedirect'>

These are configured when the configuration for this package is
executed (as long as the right dependencies are available).

Certain ZMI menus must first be available:

  >>> from zope.configuration import xmlconfig
  >>> _ = xmlconfig.string(r"""
  ...  <configure xmlns="http://namespaces.zope.org/browser" i18n_domain="zope">
  ...    <include package="zope.browsermenu" file="meta.zcml" />
  ...    <menu
  ...       id="zmi_views"
  ...       title="Views"
  ...       />
  ...
  ...    <menu
  ...       id="zmi_actions"
  ...       title="Actions"
  ...       />
  ...  </configure>
  ... """)

Now we can configure the package:

  >>> _ = xmlconfig.string(r"""
  ...  <configure xmlns="http://namespaces.zope.org/zope">
  ...    <include package="zope.app.error" />
  ...  </configure>
  ... """)
