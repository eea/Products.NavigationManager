""" Tool
"""
from Products.Archetypes import atapi
from Products.Archetypes.public import BaseFolder, BaseFolderSchema
from Products.NavigationManager.config import PROJECTNAME

# additional imports from tagged value 'import'
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import UniqueObject
from plone.memoize.ram import cache, global_cache

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from Products.CMFDynamicViewFTI.interfaces import ISelectableBrowserDefault
from Products.statusmessages.interfaces import IStatusMessage

def cacheKeyGetTree(method, self, site, tabselected='default'):
    """ Cache key
    """
    request = self.REQUEST
    if tabselected != 'default':
        secondkey = tabselected
    else:
        secondkey = request.get('ACTUAL_URL').split('/')
        if len(secondkey) > 5:
            secondkey = secondkey[:5]
    return (site, secondkey, request.get('LANGUAGE', 'en'))

class NavigationManager(UniqueObject, BaseFolder):
    """ Navigation manager
    """

    meta_type = archetype_name = portal_type = 'NavigationManager'
    allowed_content_types = ['NavigationItem']
    filter_content_types = 1
    global_allow = 0
    allow_discussion = False
    immediate_view = 'base_view'
    default_view = 'base_view'
    schema = BaseFolderSchema.copy()

    # Methods
    def selectViewTemplate(self, context, templateId):
        """ Helper method to select a view template.

        Returns action status
        """
        if not ISelectableBrowserDefault.providedBy(context):
            msg = _(u'Object does not support selecting layout templates')
            IStatusMessage(context.REQUEST).addStatusMessage(msg, 'error')
            return 'failure'

        context.setLayout(templateId)
        notify(ObjectModifiedEvent(context))

        msg = _(u'View changed.')
        IStatusMessage(context.REQUEST).addStatusMessage(msg, 'info')
        return 'success'

    def saveDefaultPage(self, context, objectId=None):
        """ Helper method to select a default page for a folder view.

        Returns action status
        """
        if not objectId:
            msg = _(u'Please select an item to use.')
            IStatusMessage(context.REQUEST).addStatusMessage(msg, 'error')
            return 'missing'

        if not ISelectableBrowserDefault.providedBy(context):
            raise NotImplementedError(
                "Object does not support setting default page")

        # Also should never happen
        if objectId not in context.objectIds():
            msg = _(
                u'There is no object with short name ${name} in this folder.',
                mapping={u'name' : objectId})

            IStatusMessage(context.REQUEST).addStatusMessage(msg, 'error')
            return 'failure'

        context.setDefaultPage(objectId)
        notify(ObjectModifiedEvent(context))

        msg = _(u'View changed.')
        IStatusMessage(context.REQUEST).addStatusMessage(msg, 'info')
        return 'success'

    @cache(cacheKeyGetTree)
    def getTree(self, site, tabselected='default'):
        """
        It returns a list  of menu items objects from the root of this menu manager.
        Useful to generate top navigation like portal tabs.
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        request = self.REQUEST
        actualUrl = request.get('ACTUAL_URL')
        local = False
        if actualUrl.startswith( portal.absolute_url() ):
            local = True

        fallback = getattr(self, 'navigationmanager_fallback', False)

        tree = []
        node = getattr(self, site, None)
        language = None
        if node is not None:
            if fallback:
                language = request.get('LANGUAGE', None)
                canonical = node.getCanonical()
                if canonical is not None and canonical is not node:
                    node = canonical
            tree, _selected = node.getTree(local, tabselected, language)
        return tree


def register():
    """ Register custom content-type
    """
    atapi.registerType(NavigationManager, PROJECTNAME)

def invalidateNavigationManagerTreeCache(obj, event):
    """ Invalidate cache
    """
    global_cache.invalidate(
        'Products.NavigationManager.NavigationManager.getTree')
