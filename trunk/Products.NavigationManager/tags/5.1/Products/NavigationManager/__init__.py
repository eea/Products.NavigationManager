""" Init
"""
from Products.CMFCore import utils as cmfutils

from Products.Archetypes import atapi
from Products.NavigationManager.config import PROJECTNAME
from Products.NavigationManager import NavigationItem
from Products.NavigationManager import NavigationManager

def initialize(context):
    """ Zope 2
    """
    # Register AT Content-Types
    atapi.registerType(NavigationManager.NavigationManager, PROJECTNAME)
    atapi.registerType(NavigationItem.NavigationItem, PROJECTNAME)

    # Register custom content-types
    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(PROJECTNAME),
        PROJECTNAME)

    # Initialize portal tools
    cmfutils.ToolInit(
        PROJECTNAME +' Tools',
        tools = (NavigationManager.NavigationManager,),
        icon='tool.gif'
    ).initialize(context)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types = content_types,
        permission = "Add portal content",
        extra_constructors = constructors,
        fti = ftis).initialize(context)
