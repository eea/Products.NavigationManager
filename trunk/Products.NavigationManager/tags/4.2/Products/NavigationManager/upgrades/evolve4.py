""" Evolution scripts
"""
import logging
from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from Products.NavigationManager.interfaces import IHideBreadcrumbsViewlet

logger = logging.getLogger('Products.NavigationManager.upgrades')

def evolve(context):
    """ Evolve to version 4.0
    """
    # Cleanup siteproperties
    ptool = getToolByName(context, 'portal_properties')
    props = getattr(ptool, 'site_properties', None)
    nprops = getattr(ptool, 'navtree_properties', None)

    # Unhide subtypes is deprecated, delete it
    if hasattr(props, 'unhide_subtypes'):
        logger.info('Removing unhide_subtypes property from site_properties')
        props.manage_delProperties(ids=['unhide_subtypes', ])

    # hide_if_empty is deprecated, delete it
    if hasattr(props, 'hide_if_empty'):
        logger.info('Removing hide_if_empty property from site_properties')
        props.manage_delProperties(ids=['hide_if_empty', ])

    # topicListingInNavtree is deprecated, delete it
    if hasattr(nprops, 'topicListingInNavtree'):
        logger.info('Removing topicListingInNavtree from navtree_properties')
        nprops.manage_delProperties(ids=['topicListingInNavtree', ])

    # Delete is_empty catalog index/column
    ctool = getToolByName(context, 'portal_catalog')

    if 'is_empty' in ctool.indexes():
        logger.info('Removing is_empty index from portal_catalog')
        ctool.delIndex('is_empty')

    if 'is_empty' in ctool.schema():
        logger.info('Removing is_empty metadata from portal_catalog')
        ctool.delColumn('is_empty')

def fix_site_breadcrumbs(context):
    """ Hide SITE from breadcrumbs
    """
    logger.info('Hiding SITE and its translations from breadcrumbs...')
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    site = getattr(portal, 'SITE', None)

    if not site:
        logger.info('Nothing to do. Aborting...')
        return

    if not IHideFromBreadcrumbs.providedBy(site):
        logger.info('Applying IHideFromBreadcrumbs on SITE')
        alsoProvides(site, IHideFromBreadcrumbs)

    if not IHideBreadcrumbsViewlet.providedBy(site):
        logger.info('Applying IHideBreadcrumbsViewlet on SITE')
        alsoProvides(site, IHideBreadcrumbsViewlet)

    if not hasattr(site, 'getTranslations'):
        logger.info('No translations. Aborting...')
        return

    for lang in site.getTranslations():
        translation = site.getTranslation(lang)
        if not IHideFromBreadcrumbs.providedBy(translation):
            logger.info('Applying IHideFromBreadcrumbs on %s', lang)
            alsoProvides(translation, IHideFromBreadcrumbs)

        if not IHideBreadcrumbsViewlet.providedBy(translation):
            logger.info('Applying IHideBreadcrumbsViewlet on %s', lang)
            alsoProvides(translation, IHideBreadcrumbsViewlet)

    logger.info('Hiding SITE and its translations from breadcrumbs... DONE')
