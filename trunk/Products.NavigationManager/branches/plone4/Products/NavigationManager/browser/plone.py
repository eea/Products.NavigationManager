""" Plone
"""
from zope.interface import implements

try:
    from Products.EEAPloneAdmin.browser.plone import PloneAdmin
    Plone = PloneAdmin
except ImportError:
    from Products.CMFPlone.browser.ploneview import Plone

from Products.CMFPlone.browser.interfaces import IPlone
from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName

class NavigationRootPlone(Plone):
    """ Override plone portal url when in NavigationManager. Usage by calling
        http://webservices/templates/portal_navigationmanager/site/getHeader
    """

    implements(IPlone)

    def navigationRootUrl(self):
        ntool = getToolByName(self.context, 'portal_navigationmanager')
        return utils.parent(ntool).getUrl()
