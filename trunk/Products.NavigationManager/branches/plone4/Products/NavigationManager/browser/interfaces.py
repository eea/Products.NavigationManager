""" Browser interfaces
"""
from zope.interface import Interface, Attribute
from Products.CMFPlone.browser.interfaces import INavigationTree

class INavigationManagerRequest(INavigationTree):
    """ Marker interface for navigation manager request """

class INavigationManagerTree(INavigationTree):
    """ Marker interface for navigation manager tree """

class INavigationItem(Interface):
    """ Marker interface """

class IMenu(Interface):
    """ Menu
    """
    def getSubMenu(site='default', menuid=''):
        """ Goes through the menu tree and returns a list of dictionaries with
        nav info for menuid """

    def getItemUrl(self, url, relative='no'):
        """ give an url, returns absolute or relative url """

    def getPath(site='default', menuid=''):
        """ Returns a list of menu items until the menuid is found. Used for
        base pathbar. """

    def isRoot():
        """ Returns true if the context is the root of the site or if
            it is a default page of the root folder of the site."""

    def getSiteRootId():
        """ returns the id of the site root content folder """

class IContentNavigationSectionMenu(Interface):
    """ Content Navigation Section Menu
    """
    def display():
        """ Retrun true or false if the navigation section meny should be
        displayed. """

    menu = Attribute(u"Return the sections for the menu.")
