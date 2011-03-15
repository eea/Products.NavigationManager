import zope.interface

#from DateTime import DateTime
from Acquisition import aq_base

try:
    from Products.EEAPloneAdmin.browser.plone import PloneAdmin as Plone
    Plone #pyflakes
except ImportError:
    from Products.CMFPlone.browser.plone import Plone

from Products.CMFPlone.browser.plone import cache_decorator
from Products.CMFPlone.browser.interfaces import IPlone
from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName

#from Products.NavigationManager.browser.navigation import getApplicationRoot 

class NavigationRootPlone(Plone):
    """ Override plone portal url when in NavigationManager. Usage by calling
    http://webservices/templates/portal_navigationmanager/site/getHeader """

    zope.interface.implements(IPlone)
    
    def navigationRootUrl(self):
        context = utils.context(self)

        navmanager = getToolByName(context, 'portal_navigationmanager')
        obj = context
        while aq_base(utils.parent(obj)) is not aq_base(navmanager):
            obj = utils.parent(obj)

        return obj.getUrl()
    
    navigationRootUrl = cache_decorator(navigationRootUrl)
