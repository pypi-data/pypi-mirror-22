This package provides a UI to maintain hierarchical user preferences
in the ZMI.

.. contents::

=====================
 zope.app.preference
=====================

This package provides a user interface in the ZMI, so the user can edit
the preferences.

Set up
======

To show the user interface functions we need some setup beforehand:

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

As the preferences cannot be defined through the web we have to define
them in python code:

  >>> import zope.interface
  >>> import zope.schema
  >>> class IZMIUserSettings(zope.interface.Interface):
  ...     """Basic User Preferences"""
  ...
  ...     email = zope.schema.TextLine(
  ...         title=u"E-mail Address",
  ...         description=u"E-mail Address used to send notifications")
  ...
  ...     skin = zope.schema.Choice(
  ...         title=u"Skin",
  ...         description=u"The skin that should be used for the ZMI.",
  ...         values=['Rotterdam', 'ZopeTop', 'Basic'],
  ...         default='Rotterdam')
  ...
  ...     showZopeLogo = zope.schema.Bool(
  ...         title=u"Show Zope Logo",
  ...         description=u"Specifies whether Zope logo should be displayed "
  ...                     u"at the top of the screen.",
  ...         default=True)
  >>> class INotCategorySettings(zope.interface.Interface):
  ...    """An example that's not a categary"""
  ...    comment = zope.schema.TextLine(
  ...        title=u'A comment',
  ...        description=u'A description')

The preference schema is usually registered using a ZCML statement:

  >>> from zope.configuration import xmlconfig
  >>> import zope.preference
  >>> context = xmlconfig.file('meta.zcml', zope.preference)

  >>> context = xmlconfig.string('''
  ...     <configure
  ...         xmlns="http://namespaces.zope.org/zope"
  ...         i18n_domain="test">
  ...
  ...       <preferenceGroup
  ...           id="ZMISettings"
  ...           title="ZMI Settings"
  ...           schema="zope.app.preference.README.IZMIUserSettings"
  ...           category="true"
  ...           />
  ...
  ...       <preferenceGroup
  ...           id="NotCategory"
  ...           title="Not Category"
  ...           schema="zope.app.preference.README.INotCategorySettings"
  ...           category="false"
  ...           />
  ...
  ...     </configure>''', context)

Editing Preferences
===================

The preferences are accessable in the ``++preferences++`` namespace:

  >>> browser.open('http://localhost/++preferences++')

The page shows a form which allows editing the preference values:

  >>> browser.getControl("comment").value = "A comment"
  >>> browser.getControl('E-mail').value = 'hans@example.com'
  >>> browser.getControl('Skin').displayOptions
  ['Rotterdam', 'ZopeTop', 'Basic']
  >>> browser.getControl('Skin').displayValue = ['ZopeTop']
  >>> browser.getControl('Show Zope Logo').selected
  True
  >>> browser.getControl('Show Zope Logo').click()

After selecting `Change` the values get persisted:

  >>> browser.getControl('Change').click()
  >>> browser.url
  'http://localhost/++preferences++/@@index.html'
  >>> browser.getControl('E-mail').value
  'hans@example.com'
  >>> browser.getControl('Skin').displayValue
  ['ZopeTop']
  >>> browser.getControl('Show Zope Logo').selected
  False

The preference group is shown in a tree. It has a link to the form:

  >>> browser.getLink('ZMISettings').click()
  >>> browser.url
  'http://localhost/++preferences++/ZMISettings/@@index.html'
  >>> browser.getControl('E-mail').value
  'hans@example.com'


Preference Group Trees
======================

The preferences would not be very powerful, if you could create a full
preferences. So let's create a sub-group for our ZMI user settings, where we
can adjust the look and feel of the folder contents view:

  >>> class IFolderSettings(zope.interface.Interface):
  ...     """Basic Folder Settings"""
  ...
  ...     shownFields = zope.schema.Set(
  ...         title=u"Shown Fields",
  ...         description=u"Fields shown in the table.",
  ...         value_type=zope.schema.Choice(['name', 'size', 'creator']),
  ...         default=set(['name', 'size']))
  ...
  ...     sortedBy = zope.schema.Choice(
  ...         title=u"Sorted By",
  ...         description=u"Data field to sort by.",
  ...         values=['name', 'size', 'creator'],
  ...         default='name')

And register it:

  >>> context = xmlconfig.string('''
  ...     <configure
  ...         xmlns="http://namespaces.zope.org/zope"
  ...         i18n_domain="test">
  ...
  ...       <preferenceGroup
  ...           id="ZMISettings.Folder"
  ...           title="Folder Content View Settings"
  ...           schema="zope.app.preference.README.IFolderSettings"
  ...           />
  ...
  ...     </configure>''', context)

The sub-group is displayed inside the parent group as a form:

  >>> browser.reload()
  >>> browser.getControl('Shown Fields').displayOptions
  ['name', 'size', 'creator']
  >>> browser.getControl('Shown Fields').displayValue
  ['name', 'size']
  >>> browser.getControl('Shown Fields').displayValue = ['size', 'creator']
  >>> browser.getControl('Sorted By').displayOptions
  ['name', 'size', 'creator']
  >>> browser.getControl('Sorted By').displayValue = ['creator']

Selecing `Change` persists these values, too:

  >>> browser.getControl('Change').click()
  >>> browser.getControl('Shown Fields').displayValue
  ['size', 'creator']
  >>> browser.getControl('Sorted By').displayValue
  ['creator']
  >>> browser.open("http://localhost/++preferences++/ZMISettings.Folder/@@index.html")


=========
 CHANGES
=========

4.0.0 (2017-05-17)
==================

- Add support for Python 3.4, 3.5, 3.6 and PyPy.

- Removed test dependency on ``zope.app.zcmlfiles`` and
  ``zope.app.renderer``, among others. ``zope.app.renderer`` is still
  required at runtime.

- Broke test dependency on ``zope.app.testing`` by using
  ``zope.app.wsgi.testlayer``.


3.8.1 (2010-06-15)
==================

- Fixed BBB imports which pointed to a not existing `zope.preferences`
  package.


3.8.0 (2010-06-12)
==================

- Depend on split out `zope.preference`.


3.7.0 (2010-06-11)
==================

- Added HTML labels to ZMI forms.

- Removed `edit.pt` as it seems to be unused.

- Added tests for the ZMI views.


3.6.0 (2009-02-01)
==================

- Use ``zope.container`` instead of ``zope.app.container``.


3.5.0 (2009-01-17)
==================

- Got rid of ``zope.app.zapi`` dependency, replacing its uses with direct
  imports from original places.

- Change mailing address from zope3-dev to zope-dev, as the first one
  is retired now.

- Fix tests for python 2.6.

- Remove zpkg stuff and zcml include files for
  old mkzopeinstance-based instances.


3.4.1 (2007-10-30)
==================

- Avoid deprecation warnings for ``ZopeMessageFactory``.


3.4.0 (2007-10-25)
==================

- Initial release independent of the main Zope tree.


