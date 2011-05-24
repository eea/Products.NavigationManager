""" Custom breadcrumbs
"""
from zope.interface import implements
from zope.component import queryMultiAdapter
from Products.CMFPlone import utils
from Products.CMFPlone.browser.interfaces import INavigationBreadcrumbs
from Products.CMFPlone.browser.navigation import PhysicalNavigationBreadcrumbs

class Breadcrumbs(PhysicalNavigationBreadcrumbs):
    """ Custom breadcrumbs according with portal_navigationmanager
    """
    implements(INavigationBreadcrumbs)

    @property
    def site(self):
        """ Site root
        """
        return self.request.form.get('site',
                getattr(self.context, 'navigationmanager_site', 'default'))

    @property
    def menuid(self):
        """ Menuid
        """
        return self.request.form.get('menuid',
                getattr(self.context, 'navigationmanager_menuid', ''))

    def breadcrumbs(self):
        """ Breadcrumbs
        """
        ntool = utils.getToolByName(
            self.context, 'portal_navigationmanager', None)
        if not ntool:
            return super(Breadcrumbs, self).breadcrumbs()

        menu = queryMultiAdapter((self.context, self.request), name=u'eea_menu')
        if not menu:
            return ()

        if menu.isRoot():
            return ()

        rootid = menu.getSiteRootId()
        crumbs = menu.getPath(self.site, self.menuid)

        # Base breadcrumbs
        base = ()
        for crumb in crumbs:
            cid = crumb.get('id', '')
            if cid == rootid:
                continue

            url = crumb.get('url', None)
            if not url:
                continue

            title = crumb.get('title', cid)

            base += ({
                'absolute_url': url,
                'Title': title
                },)

        # Tail breadcrumbs
        plone = queryMultiAdapter((self.context, self.request), name=u'plone')
        if not plone:
            return base

        isDefault = plone.isDefaultPageInFolder()
        if not self.menuid and (menu.isRoot() or isDefault):
            return base

        base += ({
            'absolute_url': self.context.absolute_url(),
            'Title': utils.pretty_title_or_id(self.context, self.context)
            },)

        return base
