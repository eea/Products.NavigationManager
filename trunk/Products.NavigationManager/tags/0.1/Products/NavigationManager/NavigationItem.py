# File: NavigationItem.py
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
from Products.ATContentTypes.content.folder import ATFolder
#from Products.NavigationManager.config import *
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.plone import cache_decorator
from Products.NavigationManager.config import PROJECTNAME
##code-section module-header #fill in your manual code here
##/code-section module-header

schema = atapi.Schema((

    atapi.StringField(
        name='url',
        widget=atapi.StringWidget(
            label='Url',
            label_msgid='NavigationManager_label_url',
            i18n_domain='NavigationManager',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

NavigationItem_schema = getattr(ATFolder, 'schema', atapi.Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class NavigationItem(ATFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(ATFolder, '__implements__', ()), )

    # This name appears in the 'add' box
    archetype_name = 'NavigationItem'

    meta_type = 'NavigationItem'
    portal_type = 'NavigationItem'
    allowed_content_types = ['NavigationItem'] + list(getattr(ATFolder,
                                            'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    allow_discussion = False
    #content_icon = 'NavigationItem.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "NavigationItem"
    typeDescMsgId = 'description_edit_navigationitem'

    schema = NavigationItem_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getTree')
    def getTree(self, local = False, tabselected='default', language = None):
        """
        It returns a list  of menu items objects from the root of this
        menu manager. Useful to generate top navigation like portal tabs.
        """
        request = self.REQUEST
        actualUrl = request.get('ACTUAL_URL')
        url = request.get('HTTP_REFERER')
        if local or not url:
            url = actualUrl
        result = []
        subItemSelected = False
        wftool = getToolByName(self, 'portal_workflow')

        for n in self.contentValues():
            # if workflow state for this navigationitem is private or draft
            # it shouldn't show up in the menu
            state = wftool.getInfoFor(n, 'review_state')
            if state != 'published':
                continue

            children, selected = n.getTree(local, tabselected, language)

            fallback = False
            fallbackLanguage = ''
            if language is not None:
                translation = n.getTranslation(language)
                if translation is None:
                    fallback = True
                    fallbackLanguage = n.Language()
                else:
                    if wftool.getInfoFor(translation, 'review_state') != 'published':
                        # we have a translation but it's not published
                        # so we don't fallback here
                        continue
                    n = translation
                    
                    
            result.append({'item': { 'title': n.Title(),
                                     'id' : n.getId(),
                                     'description' : n.Description(),
                                     'url' : n.getUrl() },
                           'children': children,
                           'selected': selected,
                           'fallback': fallback,
                           'fallbackLanguage': fallbackLanguage })
            if selected:
                subItemSelected = True
        # Top menu selected if a subitem is selected
        translation = self.getTranslation(language)
        if language is not None and translation is not None:
            myUrl = self.getTranslation(language).getUrl()
        else:
            myUrl = self.getUrl()

        if myUrl.startswith('/'):
            url = request.get('PATH_INFO')

        selected = subItemSelected or self.getId() == tabselected or \
                tabselected == 'default' and myUrl == url
        return result, selected

    
atapi.registerType(NavigationItem, PROJECTNAME)
# end of class NavigationItem

##code-section module-footer #fill in your manual code here
##/code-section module-footer



