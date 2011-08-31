""" Browser interfaces
"""
from zope.interface import Interface

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

class IHideBreadcrumbsViewlet(Interface):
    """ Marker for content which should hide breadcrumbs viewlet
    """
