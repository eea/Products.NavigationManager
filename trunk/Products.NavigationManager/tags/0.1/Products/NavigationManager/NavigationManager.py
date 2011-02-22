# File: NavigationManager.py
#
# Copyright (c) 2006 by []
# Generator: ArchGenXML Version 1.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.Archetypes.public import BaseFolder, BaseFolderSchema
from Products.NavigationManager.config import PROJECTNAME

# additional imports from tagged value 'import'
from Products.CMFCore.utils import getToolByName


from Products.CMFCore.utils import UniqueObject

    
from plone.memoize.ram import cache, global_cache

def cacheKeyGetTree(method, self, site, tabselected='default'):
    request = self.REQUEST
    if tabselected != 'default':
        secondkey = tabselected
    else:
        secondkey = request.get('ACTUAL_URL').split('/')
        if len(secondkey) > 5:
            secondkey = secondkey[:5]
    return (site, secondkey, request.get('LANGUAGE', 'en'))


schema = atapi.Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

NavigationManager_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class NavigationManager(UniqueObject, BaseFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject, '__implements__', ()), ) + (getattr(BaseFolder, '__implements__', ()), )

    # This name appears in the 'add' box
    archetype_name = 'NavigationManager'

    meta_type = 'NavigationManager'
    portal_type = 'NavigationManager'
    allowed_content_types = ['NavigationItem']
    filter_content_types = 1
    global_allow = 0
    allow_discussion = False
    #content_icon = 'NavigationManager.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "NavigationManager"
    typeDescMsgId = 'description_edit_navigationmanager'
    #toolicon = 'NavigationManager.gif'

    schema = NavigationManager_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseFolder.__init__(self,'portal_navigationmanager')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # Methods

    security.declarePublic('getTree')
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
            tree, selected = node.getTree(local, tabselected, language)
        return tree


atapi.registerType(NavigationManager, PROJECTNAME)
# end of class NavigationManager

def invalidateNavigationManagerTreeCache(obj, event):
    global_cache.invalidate('Products.NavigationManager.NavigationManager.getTree')



