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


# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().
#   - To register a customisation policy, create a file CustomizationPolicy.py
#       with a method register(context) to register the policy.

from zLOG import LOG, INFO
LOG('NavigationManager', INFO, 'Installing Product')

try:
    import CustomizationPolicy
except ImportError:
    CustomizationPolicy = None

from Globals import package_home
from Products.CMFCore import utils as cmfutils
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore import DirectoryView
from Products.CMFPlone.PloneUtilities import ToolInit
from Products.CMFPlone.CatalogTool import registerIndexableAttribute
#from Products.Archetypes.atapi import *
from Products.Archetypes.atapi import process_types
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize
from sections import getNavSectionsForIndex
from Products.GenericSetup import EXTENSION, profile_registry
from Products.CMFPlone.interfaces import IPloneSiteRoot
import os, os.path

#from Products.NavigationManager.config import *
from Products.NavigationManager.catalog import getEmptyForIndex

from Products.NavigationManager.config import PROJECTNAME, product_globals
from Products.NavigationManager.config import DEFAULT_ADD_CONTENT_PERMISSION

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/NavigationManager',
                                    product_globals)

##code-section custom-init-head #fill in your manual code here
registerIndexableAttribute('navSection', getNavSectionsForIndex)
##/code-section custom-init-head

profile_registry.registerProfile(
                    'navigationmanager',
                    'NavigationManager',
                    'Extension profile for NavigationManager Product',
                    'profile/default',
                    'NavigationManager',
                    EXTENSION,
                    for_=IPloneSiteRoot)

# Catalog a boolean saying whether a folder is empty or not.
# This decides if the folder should be shown in navtree for
# anonymous public users.
registerIndexableAttribute('is_empty', getEmptyForIndex)

def initialize(context):
    ##code-section custom-init-top #fill in your manual code here
    ##/code-section custom-init-top

    # imports packages and types for registration

    import NavigationItem
    import NavigationManager

    # Initialize portal tools
    tools = [NavigationManager.NavigationManager]
    ToolInit( PROJECTNAME +' Tools',
                tools = tools,
                product_name = PROJECTNAME,
                icon='tool.gif'
                ).initialize( context )

    # Initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    # Apply customization-policy, if theres any
    if CustomizationPolicy and hasattr(CustomizationPolicy, 'register'):
        CustomizationPolicy.register(context)
        print 'Customization policy for NavigationManager installed'

    # this is needed so the selectViewTemplate.cpy and
    # saveDefaultPage.cpy scripts can send events
    from AccessControl import allow_module, allow_class, ModuleSecurityInfo
    from zope.app.event.objectevent import ObjectModifiedEvent
    ModuleSecurityInfo('zope.app.event.objectevent').declarePublic('ObjectModifiedEvent')
    allow_class(ObjectModifiedEvent)
    allow_module('zope.event')

    ##code-section custom-init-bottom #fill in your manual code here
    ##/code-section custom-init-bottom
