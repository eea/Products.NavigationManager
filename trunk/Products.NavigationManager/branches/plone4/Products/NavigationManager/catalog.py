""" Catalog indexes
"""
import logging
from zope.interface import Interface
from zope.component import queryUtility
from plone.indexer import indexer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr, safe_callable

try:
    from p4a.subtyper import interfaces as p4aifaces
    ISubtyper = p4aifaces.ISubtyper
except ImportError:
    class ISubtyper(Interface):
        """ ISubtyper """

logger = logging.getLogger("Products.NavigationManager.catalog")

def canBeEmpty(obj):
    """ figures out whether the object can be treaded as empty or not.
        Non-folderish objects can not be empty. Topics are dynamic so
        they can not be empty either. """

    props = getToolByName(obj, 'portal_properties')
    site_props = getattr(props, 'site_properties')
    hide_if_empty = getattr(site_props, 'hide_if_empty', ())
    hidden = obj.portal_type in hide_if_empty

    # Handle subtyped objects
    subtyper = queryUtility(ISubtyper)
    if not subtyper:
        return hidden

    unhide_subtypes = getattr(site_props, 'unhide_subtypes', ())
    etype = subtyper.existing_type(obj)
    type_name = etype and etype.name or ""

    return hidden and (type_name not in unhide_subtypes)

def indexObject(obj):
    """ Adds an object to the catalog if it's not already there.
        It only adds contentish objects by checking if the object
        has an indexObject method. Taken from CMFPlone/CatalogTool.py
    """
    if (base_hasattr(obj, 'indexObject') and safe_callable(obj.indexObject)):
        try:
            obj.indexObject()
        except TypeError, err:
            # Catalogs have 'indexObject' as well, but they
            # take different args, and will fail
            logger.info(err)

def indexChildrenIfNotIndexed(obj, catalog):
    """ Check if there are objects that are not yet indexed.
        This should only happen when we do catalog update/rebuild in ZMI
    """
    for child in obj.objectValues():
        path = '/'.join(child.getPhysicalPath())
        if catalog.getrid(path) is None:
            # the object doesn't exist in catalog, so add it
            indexObject(child)

@indexer(Interface)
def getEmptyForIndex(obj, **kwargs):
    """ is_empty index
    """
    can_be_empty = canBeEmpty(obj)

    if not can_be_empty:
        return False

    listing_views = ('folder_listing', 'folder_summary_view', 'topic_view',
                     'richtopic_view', 'atct_album_view', 'folder_tabular_view',
                     'folder_contents', 'mediacentre_view')
    if base_hasattr(obj, 'layout') and obj.getLayout() not in listing_views:
        return False

    if base_hasattr(obj, 'default_page'):
        page = obj.getDefaultPage()
        if page is not None:
            page = getattr(obj, obj.getDefaultPage(), None)
        if page is not None and not canBeEmpty(page):
            return False

    catalog = getToolByName(obj, 'portal_catalog')
    query = {'path': {'query': '/'.join(obj.getPhysicalPath()), 'depth': 1},
             'review_state': 'published' }
    portal_languages = getToolByName(obj, 'portal_languages', None)

    # the request might not contain the right language if reindexing
    # is done programmatically
    # because the results of the catalog query is language specific,
    # we need to enable language support for each object that is reindexed,
    # an "english"  view might create and reindex objects under /www/sv
    # such objects need to add Language='sv' to the query
    if portal_languages:
        old_namestack = obj.REQUEST.get('TraversalRequestNameStack', [])
        namestack = list(obj.getPhysicalPath()[2:])
        namestack.reverse()
        obj.REQUEST.set('TraversalRequestNameStack', namestack)
        portal_languages.setLanguageBindings()


    if getattr(obj, 'portal_type', None) in ('Topic', 'RichTopic'):
        if obj.queryCatalog(batch=True):
            return False
        else:
            return True

    indexChildrenIfNotIndexed(obj, catalog)
    brains = catalog.searchResults(query)
    if portal_languages:
        obj.REQUEST.set('TraversalRequestNameStack', old_namestack)
        portal_languages.setLanguageBindings()

    for brain in brains:
        if brain.getURL() == obj.absolute_url():
            # we don't care about the object that is just being reindexed
            continue

        if not canBeEmpty(brain.getObject()) or not brain.is_empty:
            # if we find a non-folder object, then the object is not empty
            return False

    return True
