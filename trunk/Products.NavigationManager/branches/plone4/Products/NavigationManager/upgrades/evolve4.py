""" Evolution scripts
"""
import logging
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('Products.NavigationManager.upgrades')

def evolve(context):
    """ Evolve to version 4.0
    """
    # Cleanup siteproperties
    ptool = getToolByName(context, 'portal_properties')
    props = getattr(ptool, 'site_properties', None)

    # Unhide subtypes is deprecated, delete it
    if hasattr(props, 'unhide_subtypes'):
        logger.info('Removing unhide_subtypes property from site_properties')
        props.manage_delProperties(ids=['unhide_subtypes', ])


    # hide_if_empty moved to navtree_properties
    if hasattr(props, 'hide_if_empty'):
        logger.info('Removing hide_if_empty property from site_properties')
        props.manage_delProperties(ids=['hide_if_empty', ])
