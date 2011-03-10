""" Init
"""
import logging
logger = logging.getLogger('Products.NavigationManager')

from Products.CMFCore import utils as cmfutils
from Products.CMFCore import DirectoryView
from Products.CMFPlone.utils import ToolInit
from Products.CMFPlone.CatalogTool import registerIndexableAttribute
from Products.Archetypes.atapi import process_types
from Products.Archetypes import listTypes
from sections import getNavSectionsForIndex
from Products.GenericSetup import EXTENSION, profile_registry
from Products.CMFPlone.interfaces import IPloneSiteRoot
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
    """ Zope 2
    """
    # imports packages and types for registration
    import NavigationItem
    import NavigationManager

    # Initialize portal tools
    tools = [NavigationManager.NavigationManager]
    ToolInit( PROJECTNAME +' Tools',
                tools = tools,
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

    # this is needed so the selectViewTemplate.cpy and
    # saveDefaultPage.cpy scripts can send events
    from AccessControl import allow_module, allow_class, ModuleSecurityInfo
    from zope.app.event.objectevent import ObjectModifiedEvent
    ModuleSecurityInfo('zope.app.event.objectevent').declarePublic(
        'ObjectModifiedEvent')
    allow_class(ObjectModifiedEvent)
    allow_module('zope.event')
