""" Custom breadcrumbs
"""
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFPlone import utils
from Products.CMFPlone.browser.interfaces import INavigationBreadcrumbs
from Products.CMFPlone.browser.navigation import PhysicalNavigationBreadcrumbs
from Products.CMFPlone.browser.navigation import get_view_url
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from Products.NavigationManager.browser.interfaces import (
    IHideBreadcrumbsViewlet,
)
from Acquisition import aq_inner
from plone.app.layout.viewlets.common import PathBarViewlet

class Breadcrumbs(PhysicalNavigationBreadcrumbs):
    """ Custom breadcrumbs
    """
    implements(INavigationBreadcrumbs)

    def breadcrumbs(self):
        """ Breadcrumbs
        """
        if ISiteRoot.providedBy(self.context):
            return ()

        context = aq_inner(self.context)
        request = self.request
        container = utils.parent(context)

        try:
            name, item_url = get_view_url(context)
        except AttributeError:
            print context
            raise

        if container is None:
            return ({'absolute_url': item_url,
                     'Title': utils.pretty_title_or_id(context, context),
                    },)

        view = getMultiAdapter((container, request), name='breadcrumbs_view')
        base = tuple(view.breadcrumbs())

        # Some things want to be hidden from the breadcrumbs
        if IHideFromBreadcrumbs.providedBy(context):
            return base

        if base:
            item_url = '%s/%s' % (base[-1]['absolute_url'], name)

        # don't show default pages in breadcrumbs
        if not utils.isDefaultPage(context, request):
            base += ({'absolute_url': item_url,
                      'Title': utils.pretty_title_or_id(context, context),
                     },)

        return base

class BreadcrumbsViewlet(PathBarViewlet):
    """ Custom breadcrumbs viewlet
    """

    @property
    def navigation_root_url(self):
        """ Override navigation root to portal url
        """
        parent = aq_inner(self.context)
        plt = getToolByName(parent, 'portal_languages')
        while not ISiteRoot.providedBy(parent):
            parent = utils.parent(parent)

        lang = ""
        if plt.getPreferredLanguage() != "en":
            lang = plt.getPreferredLanguage()

        return parent.absolute_url() + "/" + lang


    @navigation_root_url.setter
    def navigation_root_url(self, value):
        """ Read-only
        """
        return

    def render(self):
        """ Handle IHideBreadcrumbs marker interface
        """
        if IHideBreadcrumbsViewlet.providedBy(self.context):
            return ""

        # Also look in canonical
        if hasattr(self.context, 'getCanonical'):
            canonical = self.context.getCanonical()
            if IHideBreadcrumbsViewlet.providedBy(canonical):
                return ""

        return self.index()
