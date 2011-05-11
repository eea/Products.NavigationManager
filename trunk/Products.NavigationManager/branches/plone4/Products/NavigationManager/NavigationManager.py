""" Tool
"""
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import UniqueObject
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFDynamicViewFTI.interfaces import ISelectableBrowserDefault
from Products.Archetypes.public import BaseFolder, BaseFolderSchema
from Products.statusmessages.interfaces import IStatusMessage

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

class NavigationManager(UniqueObject, BaseFolder):
    """ Navigation manager
    """

    meta_type = archetype_name = portal_type = 'NavigationManager'
    schema = BaseFolderSchema.copy()

    def __init__(self, oid='portal_navigationmanager'):
        super(NavigationManager, self).__init__(oid=oid)

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
        node = getattr(self, site, None)
        if not node:
            return

        language = None
        if fallback:
            language = request.get('LANGUAGE', None)
            canonical = (node.getCanonical()
                         if hasattr(node, 'getCanonical') else node)
            if canonical and (canonical is not node):
                node = canonical

        tree, _selected = node.getTree(local, tabselected, language)
        for node in tree:
            yield node
