""" Init
"""
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import ToolInit
from Products.Archetypes.atapi import process_types
from Products.Archetypes import listTypes
from Products.NavigationManager.config import PROJECTNAME
from Products.NavigationManager import NavigationItem
from Products.NavigationManager import NavigationManager

def initialize(context):
    """ Zope 2
    """
    # Register custom content-types
    NavigationItem.register()
    NavigationManager.register()

    # Initialize portal tools
    ToolInit(
        PROJECTNAME +' Tools',
        tools = (NavigationManager.NavigationManager,),
        icon='tool.gif'
    ).initialize(context)

    # Initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types = content_types,
        permission = "Add portal content",
        extra_constructors = constructors,
        fti = ftis).initialize(context)
