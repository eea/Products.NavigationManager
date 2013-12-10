""" Tool
"""
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import UniqueObject
from Products.Archetypes.public import BaseFolder, BaseFolderSchema


class NavigationManager(UniqueObject, BaseFolder):
    """ Navigation manager
    """

    meta_type = archetype_name = portal_type = 'NavigationManager'
    schema = BaseFolderSchema.copy()

    def __init__(self, oid='portal_navigationmanager'):
        super(NavigationManager, self).__init__(oid=oid)

    def getTree(self, site, tabselected='default', recursive=True):
        """ It returns a list  of menu items objects from the root of this
            menu manager. Useful to generate top navigation like portal tabs.
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

        tree, _selected = node.getTree(local, tabselected, language,
                                       recursive=recursive)

        for node in tree:
            yield node
